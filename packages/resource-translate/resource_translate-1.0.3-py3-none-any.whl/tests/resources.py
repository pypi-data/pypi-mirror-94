from resource_translate import Translator, attr


class PersonFromObj(Translator):
    constants = {"tags": "mock-person"}
    mapping = {
        "name": "first_name",
        "billing_address": {"city": "address.town"},
        "employer": "employer",
        "missing": "absent",
    }

    @attr
    def phone(self):
        return f"+{self.resource.calling_code} {self.resource.phone_number}"

    @attr("billing_address")
    def country(self):
        if self.resource.address.country_code == "US":
            return "USA"

        return self.resource.address.country_code

    @attr("nested", "attr")
    def deep(self):
        if self.repr["billing_address"]["country"] == "USA":
            return "Deep Attribute"


class PersonFromMap(Translator):
    constants = {"tags": "mock-person"}
    mapping = {
        "name": "first_name",
        "billing_address": {"city": ("address", "town")},
        "employer": "employer",
        "missing": ("attr", "absent"),
        "empty_tuple": (),
    }

    @attr
    def phone(self):
        return f"+{self.resource['calling_code']} {self.resource['phone_number']}"

    @attr("billing_address")
    def country(self):
        if self.resource["address"]["country_code"] == "US":
            return "USA"

        return self.resource["address"]["country_code"]

    @attr("nested", "attr")
    def deep(self):
        if self.repr["billing_address"]["country"] == "USA":
            return "Deep Attribute"
