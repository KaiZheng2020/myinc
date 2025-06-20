import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path

from app.database import init_db
from app.crud import create_invoice, get_invoice
from app.models import InvoiceIn, ItemIn
from app.pdf_utils import generate_invoice_pdf
from app.main import PDF_DIR

init_db()


def test_create_invoice(tmp_path):
    PDF_DIR.mkdir(exist_ok=True)
    data = InvoiceIn(
        items=[ItemIn(name="ItemA", quantity=2, unit_price=10.0),
               ItemIn(name="ItemB", quantity=1, unit_price=20.0)],
        notes="test",
    )
    invoice_id = create_invoice(data)
    invoice, items = get_invoice(invoice_id)
    pdf_path = PDF_DIR / f"invoice_{invoice_id}.pdf"
    generate_invoice_pdf(["test"], str(pdf_path))

    assert invoice["subtotal"] == 40.0
    assert round(invoice["total_tax"], 2) == 6.0
    assert round(invoice["total"], 2) == 46.0
    assert pdf_path.exists()
