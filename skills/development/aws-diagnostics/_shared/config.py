"""
Gestione configurazione AWS per skill diagnostiche LAIF.

Carica aws-config.yaml dal progetto e risolve nomi risorse per ambiente.
"""

import os
import re
import sys


def _parse_yaml_simple(text: str) -> dict:
    """
    Parser YAML minimale per il formato aws-config.yaml.

    Gestisce solo il sottoinsieme di YAML usato nel config:
    chiavi, valori stringa (con o senza quote), e nesting basato su indentazione.
    Non supporta liste, anchor, multiline, o feature YAML avanzate.
    """
    result = {}
    # Stack: lista di (indent_level, dict_ref)
    # indent_level è l'indentazione a cui le chiavi di questo dict appaiono
    stack = [(-1, result)]

    for line in text.split("\n"):
        # Ignora commenti e righe vuote
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(stripped)

        # Risali lo stack finché non troviamo un parent con indent minore
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        current = stack[-1][1]

        # Parse key: value
        match = re.match(r'^([^:]+):\s*(.*)', stripped)
        if not match:
            continue

        key = match.group(1).strip().strip('"').strip("'")
        value = match.group(2).strip()

        # Rimuovi commenti inline
        if value and not value.startswith('"') and not value.startswith("'"):
            comment_pos = value.find(" #")
            if comment_pos >= 0:
                value = value[:comment_pos].strip()

        if value:
            # Rimuovi virgolette
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            current[key] = value
        else:
            # Chiave senza valore = nuovo dizionario annidato
            # Le chiavi figlie avranno indent > indent corrente
            new_dict = {}
            current[key] = new_dict
            stack.append((indent, new_dict))

    return result


def find_kb_root() -> str:
    """Risale la directory tree cercando CLAUDE.md come marker della KB root."""
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        if os.path.exists(os.path.join(current, "CLAUDE.md")):
            return current
        current = os.path.dirname(current)
    print("ERRORE: impossibile trovare la root della KB (cercato CLAUDE.md)")
    sys.exit(1)


def load_config(project: str, env: str, kb_root: str = None) -> dict:
    """
    Carica aws-config.yaml per un progetto e ritorna la config per l'ambiente.

    Args:
        project: nome cartella progetto in projects/
        env: 'dev' o 'prod'
        kb_root: path root KB (auto-detect se None)

    Returns:
        dict con chiavi: profile, region, account_id, app_name, customer_name, resources
        resources contiene: ecs_cluster, ecs_service, ecs_task_family, log_group,
                           rds_identifier, s3_data_bucket, s3_frontend_bucket, alb_name

    Raises:
        SystemExit se il file non esiste o l'ambiente non e' configurato.
    """
    if kb_root is None:
        kb_root = find_kb_root()

    config_path = os.path.join(kb_root, "projects", project, "aws-config.yaml")

    if not os.path.exists(config_path):
        print(f"ERRORE: {config_path} non trovato.")
        print(f"Genera il file seguendo: skills/development/aws-diagnostics/_shared/config-discovery.md")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = _parse_yaml_simple(f.read())

    if "environments" not in config:
        print(f"ERRORE: aws-config.yaml non contiene 'environments'")
        sys.exit(1)

    if env not in config["environments"]:
        available = ", ".join(config["environments"].keys())
        print(f"ERRORE: ambiente '{env}' non trovato. Disponibili: {available}")
        sys.exit(1)

    return config["environments"][env]


def get_resource(config: dict, resource_name: str) -> str:
    """
    Ritorna il nome di una risorsa AWS dalla config.

    Args:
        config: dizionario ritornato da load_config()
        resource_name: chiave in config['resources'] (es. 'ecs_cluster')

    Returns:
        Nome della risorsa AWS.
    """
    resources = config.get("resources", {})
    if resource_name not in resources:
        available = ", ".join(resources.keys())
        print(f"ERRORE: risorsa '{resource_name}' non trovata. Disponibili: {available}")
        sys.exit(1)
    return resources[resource_name]
