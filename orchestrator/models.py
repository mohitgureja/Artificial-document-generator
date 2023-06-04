from pydantic import BaseModel
from pydantic.dataclasses import dataclass


# @dataclass
# class ProductData(BaseModel):
#     product_name: bool | None = None
#     product_amount: int | None = None


# @dataclass
class InvoiceData(BaseModel):
    address: bool = False
    rechnungsnummer: bool = False
    product: bool = False
    customer_name: bool = False
    organization: bool = False

    def get_variables(self):
        return vars(self)


# @dataclass
class RequestBody(BaseModel):
    invoice_params: InvoiceData | None = None
    invoice_count: int
    groundtruth_type: str
    countries: list[str]
