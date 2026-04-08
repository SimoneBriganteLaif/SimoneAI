#!/usr/bin/env python3
"""
Estrazione dati marginalità progetti LAIF dal DB Wolico.
Genera i file JSON consumati dalla dashboard HTML.

Uso: python3 extract.py
Richiede: .env con DATABASE_URL, psycopg2-binary
"""

import json
import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")
DATABASE_URL = os.environ["DATABASE_URL"]


def json_serial(obj):
    """Serializzatore JSON per tipi non standard."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def write_json(filename: str, data):
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=json_serial)
    print(f"  → {path} ({len(data)} records)")


def extract_projects(cur):
    """Classifica marginalità completa per ogni progetto."""
    cur.execute("""
        WITH employee_cost AS (
            SELECT
                ec.id_employee,
                ec.dat_start,
                COALESCE(ec.dat_end, '2099-12-31'::date) AS dat_end,
                CASE
                    WHEN ec.contract_type = 'partita_iva' THEN ec.amt_hourly_compensation
                    ELSE ec.amt_ral / 1760.0
                END AS hourly_cost
            FROM prs.employees_contracts ec
            WHERE ec.amt_ral IS NOT NULL OR ec.amt_hourly_compensation IS NOT NULL
        ),
        reporting_cost AS (
            SELECT
                r.id_sale,
                r.id_employee,
                r.num_hours,
                COALESCE(r.dat_day, r.dat_month) AS effective_day,
                r.num_hours * ec.hourly_cost AS cost
            FROM prs.reporting r
            JOIN employee_cost ec
                ON ec.id_employee = r.id_employee
                AND COALESCE(r.dat_day, r.dat_month) >= ec.dat_start
                AND COALESCE(r.dat_day, r.dat_month) <= COALESCE(ec.dat_end, '2099-12-31'::date)
            WHERE r.id_sale IS NOT NULL
              AND r.id_category IN (8, 9)
        ),
        project_agg AS (
            SELECT
                id_sale,
                SUM(num_hours) AS hours,
                ROUND(SUM(cost)::numeric, 2) AS internal_cost,
                COUNT(DISTINCT id_employee) AS num_people,
                MIN(effective_day) AS first_day,
                MAX(effective_day) AS last_day
            FROM reporting_cost
            GROUP BY id_sale
        ),
        -- Dettaglio ore per persona per progetto
        person_detail AS (
            SELECT
                rc.id_sale,
                rc.id_employee,
                e.des_name || ' ' || e.des_surname AS employee_name,
                e.des_role,
                SUM(rc.num_hours) AS hours,
                ROUND(SUM(rc.cost)::numeric, 2) AS cost
            FROM reporting_cost rc
            JOIN prs.employees e ON rc.id_employee = e.id
            GROUP BY rc.id_sale, rc.id_employee, e.des_name, e.des_surname, e.des_role
        )
        SELECT
            s.id AS sale_id,
            l.name AS project,
            p.name AS client,
            s.company,
            tl.des_name || ' ' || tl.des_surname AS team_leader,
            s.dat_order,
            s.status,
            s.flg_active,
            s.amt_untaxed AS revenue,
            COALESCE(s.amt_external_cost, 0) AS external_cost,
            COALESCE(pa.internal_cost, 0) AS internal_cost,
            s.amt_untaxed - COALESCE(pa.internal_cost, 0) - COALESCE(s.amt_external_cost, 0) AS margin,
            CASE WHEN s.amt_untaxed > 0
                THEN ROUND(((s.amt_untaxed - COALESCE(pa.internal_cost, 0) - COALESCE(s.amt_external_cost, 0)) / s.amt_untaxed * 100)::numeric, 1)
                ELSE 0
            END AS margin_pct,
            ROUND((s.amt_untaxed / 650)::numeric, 1) AS days_target,
            ROUND((COALESCE(pa.hours, 0) / 8.0)::numeric, 1) AS days_actual,
            ROUND((COALESCE(pa.hours, 0) / 8.0 - s.amt_untaxed / 650)::numeric, 1) AS days_overrun,
            COALESCE(pa.hours, 0) AS total_hours,
            COALESCE(pa.num_people, 0) AS num_people,
            pa.first_day,
            pa.last_day,
            COALESCE(
                (SELECT json_agg(json_build_object(
                    'employee', pd.employee_name,
                    'role', pd.des_role,
                    'hours', pd.hours,
                    'cost', pd.cost
                ) ORDER BY pd.cost DESC)
                FROM person_detail pd WHERE pd.id_sale = s.id),
                '[]'::json
            ) AS people_detail
        FROM prs.sales s
        JOIN prs.leads l ON s.id_lead = l.id
        LEFT JOIN prs.partners p ON l.id_partner = p.id
        LEFT JOIN prs.employees tl ON s.id_team_leader = tl.id
        LEFT JOIN project_agg pa ON pa.id_sale = s.id
        WHERE s.flg_real = true AND s.flg_official = true AND s.amt_untaxed > 0
        ORDER BY margin_pct ASC
    """)
    columns = [desc[0] for desc in cur.description]
    rows = []
    for row in cur.fetchall():
        d = dict(zip(columns, row))
        # people_detail è già JSON dal DB
        if isinstance(d["people_detail"], str):
            d["people_detail"] = json.loads(d["people_detail"])
        rows.append(d)
    return rows


def extract_timesheet(cur):
    """Ore settimanali per persona/progetto — per heatmap e curva cumulativa."""
    cur.execute("""
        SELECT
            r.id_sale,
            l.name AS project,
            r.id_employee,
            e.des_name || ' ' || e.des_surname AS employee,
            r.dat_month,
            r.num_week,
            MIN(COALESCE(r.dat_day, r.dat_month)) AS week_start,
            SUM(r.num_hours) AS hours
        FROM prs.reporting r
        JOIN prs.employees e ON r.id_employee = e.id
        LEFT JOIN prs.sales s ON r.id_sale = s.id
        LEFT JOIN prs.leads l ON s.id_lead = l.id
        WHERE r.id_category IN (8, 9)
          AND r.id_sale IS NOT NULL
        GROUP BY r.id_sale, l.name, r.id_employee, e.des_name, e.des_surname, r.dat_month, r.num_week
        ORDER BY r.dat_month, r.num_week, l.name, e.des_name
    """)
    columns = [desc[0] for desc in cur.description]
    return [dict(zip(columns, row)) for row in cur.fetchall()]


def extract_employees(cur):
    """Anagrafica dipendenti + costo orario attuale + saturazione da monthly_recap."""
    cur.execute("""
        WITH current_contract AS (
            SELECT DISTINCT ON (ec.id_employee)
                ec.id_employee,
                ec.contract_type,
                ec.amt_ral,
                ec.amt_hourly_compensation,
                CASE
                    WHEN ec.contract_type = 'partita_iva' THEN ec.amt_hourly_compensation
                    ELSE ec.amt_ral / 1760.0
                END AS hourly_cost,
                ec.dat_start,
                ec.dat_end
            FROM prs.employees_contracts ec
            WHERE ec.amt_ral IS NOT NULL OR ec.amt_hourly_compensation IS NOT NULL
            ORDER BY ec.id_employee, ec.dat_start DESC
        ),
        saturation AS (
            SELECT
                mrd.id_employee,
                mr.dat_month,
                mrd.num_worked_hours,
                mrd.num_worked_sold_hours,
                mrd.num_absence_hours,
                mrd.num_overtime_hours,
                CASE WHEN mrd.num_worked_hours > 0
                    THEN ROUND((mrd.num_worked_sold_hours::numeric / mrd.num_worked_hours * 100), 1)
                    ELSE 0
                END AS utilization_pct
            FROM prs.monthly_recap_details mrd
            JOIN prs.monthly_recap mr ON mrd.id_monthly_recap = mr.id
        ),
        -- Context switching: progetti per persona per settimana
        weekly_projects AS (
            SELECT
                r.id_employee,
                r.dat_month,
                r.num_week,
                COUNT(DISTINCT r.id_sale) AS num_projects
            FROM prs.reporting r
            WHERE r.id_sale IS NOT NULL AND r.id_category IN (8, 9)
            GROUP BY r.id_employee, r.dat_month, r.num_week
        )
        SELECT
            e.id AS employee_id,
            e.des_name || ' ' || e.des_surname AS name,
            e.des_role AS role,
            e.company,
            e.flg_operations,
            e.flg_team_leader,
            cc.contract_type,
            cc.hourly_cost,
            cc.amt_ral,
            -- Saturazione mensile
            COALESCE(
                (SELECT json_agg(json_build_object(
                    'month', s.dat_month,
                    'hours_worked', s.num_worked_hours,
                    'hours_sold', s.num_worked_sold_hours,
                    'hours_absence', s.num_absence_hours,
                    'hours_overtime', s.num_overtime_hours,
                    'utilization_pct', s.utilization_pct
                ) ORDER BY s.dat_month)
                FROM saturation s WHERE s.id_employee = e.id),
                '[]'::json
            ) AS monthly_saturation,
            -- Context switching settimanale
            COALESCE(
                (SELECT json_agg(json_build_object(
                    'month', wp.dat_month,
                    'week', wp.num_week,
                    'num_projects', wp.num_projects
                ) ORDER BY wp.dat_month, wp.num_week)
                FROM weekly_projects wp WHERE wp.id_employee = e.id),
                '[]'::json
            ) AS weekly_context_switching
        FROM prs.employees e
        LEFT JOIN current_contract cc ON cc.id_employee = e.id
        WHERE e.flg_operations = true
        ORDER BY e.des_surname, e.des_name
    """)
    columns = [desc[0] for desc in cur.description]
    rows = []
    for row in cur.fetchall():
        d = dict(zip(columns, row))
        for key in ("monthly_saturation", "weekly_context_switching"):
            if isinstance(d[key], str):
                d[key] = json.loads(d[key])
        rows.append(d)
    return rows


def extract_client_concentration(cur):
    """Revenue e margine aggregati per cliente — per Pareto chart."""
    cur.execute("""
        WITH employee_cost AS (
            SELECT
                ec.id_employee,
                ec.dat_start,
                COALESCE(ec.dat_end, '2099-12-31'::date) AS dat_end,
                CASE
                    WHEN ec.contract_type = 'partita_iva' THEN ec.amt_hourly_compensation
                    ELSE ec.amt_ral / 1760.0
                END AS hourly_cost
            FROM prs.employees_contracts ec
            WHERE ec.amt_ral IS NOT NULL OR ec.amt_hourly_compensation IS NOT NULL
        ),
        reporting_cost AS (
            SELECT r.id_sale, r.num_hours * ec.hourly_cost AS cost
            FROM prs.reporting r
            JOIN employee_cost ec
                ON ec.id_employee = r.id_employee
                AND COALESCE(r.dat_day, r.dat_month) >= ec.dat_start
                AND COALESCE(r.dat_day, r.dat_month) <= COALESCE(ec.dat_end, '2099-12-31'::date)
            WHERE r.id_sale IS NOT NULL AND r.id_category IN (8, 9)
        ),
        project_cost AS (
            SELECT id_sale, ROUND(SUM(cost)::numeric, 2) AS internal_cost
            FROM reporting_cost GROUP BY id_sale
        )
        SELECT
            p.name AS client,
            COUNT(*) AS num_projects,
            SUM(s.amt_untaxed) AS total_revenue,
            SUM(COALESCE(pc.internal_cost, 0) + COALESCE(s.amt_external_cost, 0)) AS total_cost,
            SUM(s.amt_untaxed - COALESCE(pc.internal_cost, 0) - COALESCE(s.amt_external_cost, 0)) AS total_margin,
            CASE WHEN SUM(s.amt_untaxed) > 0
                THEN ROUND((SUM(s.amt_untaxed - COALESCE(pc.internal_cost, 0) - COALESCE(s.amt_external_cost, 0)) / SUM(s.amt_untaxed) * 100)::numeric, 1)
                ELSE 0
            END AS avg_margin_pct
        FROM prs.sales s
        JOIN prs.leads l ON s.id_lead = l.id
        LEFT JOIN prs.partners p ON l.id_partner = p.id
        LEFT JOIN project_cost pc ON pc.id_sale = s.id
        WHERE s.flg_real = true AND s.flg_official = true AND s.amt_untaxed > 0
        GROUP BY p.name
        ORDER BY total_revenue DESC
    """)
    columns = [desc[0] for desc in cur.description]
    return [dict(zip(columns, row)) for row in cur.fetchall()]


def main():
    print("Connessione al DB...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("\n1. Estrazione marginalità progetti...")
    projects = extract_projects(cur)
    write_json("projects.json", projects)

    print("\n2. Estrazione timesheet settimanale...")
    timesheet = extract_timesheet(cur)
    write_json("timesheet.json", timesheet)

    print("\n3. Estrazione dipendenti + saturazione...")
    employees = extract_employees(cur)
    write_json("employees.json", employees)

    print("\n4. Estrazione concentrazione clienti...")
    clients = extract_client_concentration(cur)
    write_json("clients.json", clients)

    # Crea annotations.json vuoto se non esiste
    annotations_path = DATA_DIR / "annotations.json"
    if not annotations_path.exists():
        write_json("annotations.json", {})
        print("  → annotations.json creato (vuoto)")

    cur.close()
    conn.close()
    print("\n✓ Estrazione completata!")


if __name__ == "__main__":
    main()
