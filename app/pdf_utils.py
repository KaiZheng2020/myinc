from datetime import datetime
from typing import List

# Minimal PDF generator based on PDF specification

def _build_pdf(text_lines: List[str]) -> bytes:
    objects = []
    offsets = []

    def add_obj(content: str) -> int:
        offsets.append(sum(len(o) for o in objects))
        objects.append(content)
        return len(offsets)

    # object 1: catalog
    add_obj("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # object 2: pages
    add_obj("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")

    # build page content stream
    contents = "BT\n/F1 12 Tf\n"
    y = 750
    for line in text_lines:
        safe = line.replace('(', r'\\(').replace(')', r'\\)')
        contents += f"1 0 0 1 50 {y} Tm ({safe}) Tj\n"
        y -= 20
    contents += "ET"

    stream = f"4 0 obj\n<< /Length {len(contents)} >>\nstream\n{contents}\nendstream\nendobj\n"

    # object 3: page
    add_obj(
        "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    )
    add_obj(stream)
    # object 5: font
    add_obj("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # build xref table
    xref_start = sum(len(o) for o in objects)
    xref = ["xref\n0 {0}\n0000000000 65535 f \n".format(len(objects)+1)]
    for off in offsets:
        xref.append(f"{off:010d} 00000 n \n")
    xref_table = ''.join(xref)

    trailer = (
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n" +
        f"{xref_start}\n%%EOF"
    )

    pdf_content = ''.join(objects) + xref_table + trailer
    return pdf_content.encode('latin1')


def generate_invoice_pdf(text_lines: List[str], path: str):
    pdf_bytes = _build_pdf(text_lines)
    with open(path, 'wb') as f:
        f.write(pdf_bytes)
