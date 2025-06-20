from pydantic import BaseModel, Field, validator
from typing import List, Optional

DEFAULT_TAX_RATE = 0.15

class ItemIn(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    tax_rate: Optional[float] = None

    @validator('tax_rate', pre=True, always=True)
    def set_tax_rate(cls, v):
        return DEFAULT_TAX_RATE if v is None else v

class InvoiceIn(BaseModel):
    items: List[ItemIn]
    notes: Optional[str] = None
    tax_rate: Optional[float] = None

    @validator('tax_rate', pre=True, always=True)
    def set_tax_rate(cls, v):
        return DEFAULT_TAX_RATE if v is None else v

class ItemOut(BaseModel):
    name: str
    quantity: int
    unit_price: float
    total: float

class InvoiceOut(BaseModel):
    id: int
    subtotal: float
    total_tax: float
    total: float
    pdf_path: str
    items: List[ItemOut]

