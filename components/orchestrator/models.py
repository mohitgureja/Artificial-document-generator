from enum import Enum

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
    organization_address: bool = False
    organization_contact: bool = False
    amount_sentence: bool = False
    total_amount: bool = False
    bank_iban: bool = False
    bank_swift: bool = False
    date: bool = False
    title: bool = False
    diagnose: bool = False
    logo_image: bool = False

    # image: bool = False

    def get_variables(self):
        return vars(self)

    def set_variables(self):
        if self.product_name and self.product_amount:
            self.total_amount = True

        if self.organization:
            self.title = True


class ResumeData(BaseModel):
    name: bool = False,
    address: bool = False,
    email: bool = False,
    phone_number: bool = False,
    summary: bool = False,
    position: bool = False,
    company: bool = False,
    company_location: bool = False,
    experience_dates: bool = False,
    responsibilities: bool = False,
    project_title: bool = False,
    project_dates: bool = False,
    project_description: bool = False,
    degree: bool = False,
    school: bool = False,
    school_location: bool = False,
    graduation_date: bool = False,
    skill: bool = False,
    certificate_name: bool = False,
    date_earned: bool = False,
    language: bool = False
    profile_image: bool = False

    def get_variables(self):
        return vars(self)

    def set_variables(self):
        # if self.product_name and self.product_amount:
        #     self.total_amount = True
        return True


# @dataclass
class RequestBody(BaseModel):
    invoice_params: InvoiceData | None = None
    resume_params: ResumeData | None = None
    count: int
    groundtruth_type: str
    groundtruth_format: str
    countries: list[str]


class Params(Enum):
    invoice = "invoice"
    resume = "resume"
