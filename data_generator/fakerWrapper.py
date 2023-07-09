from faker import Faker
from faker.providers import BaseProvider


class MyProvider(BaseProvider):
    __provider__ = "product_category"
    item_categories = ["Bandages", "Syringes", "Surgical masks", "Wheelchairs", "Stethoscopes", "Thermometers",
                       "Gloves", "Blood pressure monitors",
                       "IV (intravenous) catheters", "Surgical instruments", "X-ray machines", "Ultrasound machines",
                       "MRI (magnetic resonance imaging) machines",
                       "Defibrillators", "Artificial limbs (prosthetics)", "Hearing aids"]

    def product_category(self):
        return self.random_element(self.item_categories)


def generate_fake_data(data_field, countries):
    faker = Faker(countries)
    faker.add_provider(MyProvider)
    data_dict = get_data_dict(faker)
    return data_dict[data_field]


def get_data_dict(faker):
    data = {"customer_name": faker.name(), "address": faker.address(), "organization": faker.company(),
            "product_name": faker.product_category(),
            "product_amount": faker.pricetag(), "rechnungsnummer": faker.random_int(min=100000, max=999999)}
    return data
