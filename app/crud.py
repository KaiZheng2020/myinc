from datetime import datetime
from typing import List

from .database import get_connection
from .models import InvoiceIn, ItemIn, DEFAULT_TAX_RATE


def create_invoice(data: InvoiceIn) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    subtotal = sum(item.quantity * item.unit_price for item in data.items)
    tax_rate = data.tax_rate if data.tax_rate is not None else DEFAULT_TAX_RATE
    total_tax = subtotal * tax_rate
    total = subtotal + total_tax
    cursor.execute(
        "INSERT INTO invoices(date, tax_rate, subtotal, total_tax, total, notes) "
        "VALUES(?,?,?,?,?,?)",
        (
            datetime.utcnow().isoformat(),
            tax_rate,
            subtotal,
            total_tax,
            total,
            data.notes,
        ),
    )
    invoice_id = cursor.lastrowid
    for item in data.items:
        item_total = item.quantity * item.unit_price
        cursor.execute(
            "INSERT INTO items(invoice_id, name, quantity, unit_price, total) "
            "VALUES(?,?,?,?,?)",
            (
                invoice_id,
                item.name,
                item.quantity,
                item.unit_price,
                item_total,
            ),
        )
    conn.commit()
    conn.close()
    return invoice_id


def get_invoice(invoice_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    invoice = cursor.execute(
        "SELECT * FROM invoices WHERE id=?", (invoice_id,)
    ).fetchone()
    items = cursor.execute(
        "SELECT name, quantity, unit_price, total FROM items WHERE invoice_id=?",
        (invoice_id,),
    ).fetchall()
    conn.close()
    return invoice, items
