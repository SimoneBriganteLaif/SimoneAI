---
tags: [convenzioni, database, laif-kb]
---

# Convenzioni Naming — Database

Tutti i progetti LAIF usano PostgreSQL con SQLAlchemy 2.0. Le colonne seguono un sistema di prefissi che indica il tipo di dato.

## Prefissi colonne

| Prefisso | Significato | Tipo SQL | Esempio |
|----------|-------------|----------|---------|
| `id_` | Primary/Foreign key | `Integer` / `UUID` | `id_user`, `id_order` |
| `cod_` | Codici e identificatori | `String` | `cod_order`, `cod_fiscal` |
| `des_` | Descrizioni e testi | `String` / `Text` | `des_product`, `des_note` |
| `dat_` | Date (senza ora) | `Date` | `dat_birth`, `dat_expiry` |
| `tms_` | Timestamp (con ora) | `DateTime` | `tms_created`, `tms_updated` |
| `val_` | Valori numerici | `Integer` / `Float` | `val_quantity`, `val_score` |
| `amt_` | Importi monetari | `Numeric(precision, scale)` | `amt_total`, `amt_discount` |
| `flg_` | Boolean (flag) | `Boolean` | `flg_active`, `flg_deleted` |

## Regole generali

- I nomi delle tabelle sono in **snake_case**, **plurale inglese** (es. `users`, `order_items`)
- Ogni tabella ha `id_[nome_tabella_singolare]` come primary key
- Le foreign key usano `id_[tabella_riferita_singolare]`
- Timestamp di audit: `tms_created` e `tms_updated` su ogni tabella
- Soft delete: `flg_deleted` + `tms_deleted` (dove applicabile)
- Tutti i modelli vanno in `backend/src/template/models.py` (file centralizzato)

## Esempio

```python
class Order(Base):
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    cod_order = Column(String, unique=True)
    des_note = Column(Text, nullable=True)
    amt_total = Column(Numeric(12, 2))
    val_quantity = Column(Integer)
    dat_delivery = Column(Date, nullable=True)
    flg_active = Column(Boolean, default=True)
    tms_created = Column(DateTime, server_default=func.now())
    tms_updated = Column(DateTime, onupdate=func.now())
```
