from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .models import InvoiceIn, InvoiceOut, ItemOut
from .crud import create_invoice, get_invoice
from .pdf_utils import generate_invoice_pdf

init_db()
app = FastAPI(title="Invoice Service")

PDF_DIR = Path('invoices')
PDF_DIR.mkdir(exist_ok=True)

@app.post('/invoices', response_model=InvoiceOut)
def create_invoice_endpoint(data: InvoiceIn):
    invoice_id = create_invoice(data)
    invoice, items = get_invoice(invoice_id)
    text_lines = [
        f"Invoice ID: {invoice['id']}",
        f"Date: {invoice['date']}",
    ]
    for item in items:
        text_lines.append(
            f"{item['name']} x{item['quantity']} @ {item['unit_price']} = {item['total']}"
        )
    text_lines.append(f"Subtotal: {invoice['subtotal']}")
    text_lines.append(f"Tax: {invoice['total_tax']}")
    text_lines.append(f"Total: {invoice['total']}")
    if invoice['notes']:
        text_lines.append(f"Notes: {invoice['notes']}")

    pdf_path = PDF_DIR / f"invoice_{invoice_id}.pdf"
    generate_invoice_pdf(text_lines, str(pdf_path))

    response_items = [ItemOut(**dict(row)) for row in items]
    return InvoiceOut(
        id=invoice['id'],
        subtotal=invoice['subtotal'],
        total_tax=invoice['total_tax'],
        total=invoice['total'],
        pdf_path=str(pdf_path),
        items=response_items,
    )


@app.get('/invoices/{invoice_id}', response_class=FileResponse)
def get_invoice_pdf(invoice_id: int):
    pdf_path = PDF_DIR / f"invoice_{invoice_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Invoice not found")
    return FileResponse(str(pdf_path), media_type='application/pdf')
