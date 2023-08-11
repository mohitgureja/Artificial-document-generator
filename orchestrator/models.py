from pydantic import BaseModel


# @dataclass
# class ProductData(BaseModel):
#     product_name: bool | None = None
#     product_amount: int | None = None

# @dataclass
class InvoiceData(BaseModel):
    address: bool = False
    rechnungsnummer: bool = False
    product_name: bool = False
    product_amount: bool = False
    customer_name: bool = False
    organization: bool = False
    amount_sentence: bool = False
    total_amount: bool = False

    def get_variables(self):
        return vars(self)

    def set_variables(self):
        if self.product_name and self.product_amount:
            self.total_amount = True


# @dataclass
class RequestBody(BaseModel):
    invoice_params: InvoiceData | None = None
    invoice_count: int
    groundtruth_type: str
    countries: list[str]
