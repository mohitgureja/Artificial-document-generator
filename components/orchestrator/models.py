from typing import Optional

from pydantic import BaseModel


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
    skills: bool = False,
    certificate_name: bool = False,
    date_earned: bool = False,
    languages: bool = False,
    profile_image: bool = False,
    resume_query: bool = False

    def get_variables(self):
        return vars(self)

    def set_variables(self):
        return True


def get_invoice_params(request_body):
    request_body.invoice_params.set_variables()
    params = request_body.invoice_params.get_variables()
    return {k: v for k, v in params.items() if v is True}


def get_resume_params(request_body):
    request_body.resume_params.set_variables()
    params = request_body.resume_params.get_variables()
    return {k: v for k, v in params.items() if v is True}


# @dataclass
class RequestBody(BaseModel):
    invoice_params: Optional[InvoiceData] = None
    resume_params: Optional[ResumeData] = None
    count: int
    augmentation: bool = False
    data_rendering: bool = False
    gpt_enabled: bool = False
    groundtruth_type: str
    groundtruth_format: str
    countries: list[str]


params_method = {
    "invoice": get_invoice_params,
    "resume": get_resume_params
}
