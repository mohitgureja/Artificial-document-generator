from faker import Faker
from faker.providers import BaseProvider


class MyProvider(BaseProvider):
    __provider__ = "diagnose"
    item_categories = ["Diabetes mellitus Typ 2", "Rheumatoide Arthritis", "Lungenentzündung", "Migräne", "Brustkrebs",
                       "Depression", "Asthma", "Osteoporose", "Hypertonie (Bluthochdruck)", "Schlaganfall",
                       "Magengeschwür", "Nierenstein", "Schilddrüsenunterfunktion (Hypothyreose)",
                       "Gicht", "Chronisch obstruktive Lungenerkrankung (COPD)", "Akute Pankreatitis",
                       "Herzinfarkt (Myokardinfarkt)", "Multiple Sklerose", "Parkinson-Krankheit",
                       "Alzheimer-Krankheit"]

    def diagnose(self):
        return self.random_element(self.item_categories)


def generate_fake_data(countries):
    faker = Faker(countries)
    faker.add_provider(MyProvider)
    data_dict = get_data_dict(faker)
    return data_dict


def get_data_dict(faker):
    data = {"customer_name": faker.name(), "address": faker.address(), "organization": faker.company(),
            "organization_address": faker.address(),
            "organization_contact": faker.phone_number(), "date": faker.date(), "bank_iban": faker.iban(),
            "bank_swift": faker.swift11(use_dataset=True),
            "diagnose": faker.diagnose(),
            "product_amount": faker.pricetag(), "rechnungsnummer": faker.random_int(min=100000, max=999999)}

    return data
