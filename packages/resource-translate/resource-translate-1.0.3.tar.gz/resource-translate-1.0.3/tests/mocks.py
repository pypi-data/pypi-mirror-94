class _MockAddressI:
    town = "Bobtonville"
    country_code = "US"


_MOCK_ADDRESS_I = {"town": "Bobtonville", "country_code": "US"}


class _MockAddressII:
    town = "Bobtonville"
    country_code = "MX"


_MOCK_ADDRESS_II = {"town": "Bobtonville", "country_code": "MX"}


class MockPersonI:
    first_name = "Bob"
    calling_code = 1
    phone_number = "(916) 276-6782"
    employer = None
    address = _MockAddressI


MOCK_PERSON_I = {
    "first_name": "Bob",
    "calling_code": 1,
    "phone_number": "(916) 276-6782",
    "employer": None,
    "address": _MOCK_ADDRESS_I,
}


class MockPersonII:
    first_name = "Bob"
    calling_code = 1
    phone_number = "(916) 276-6782"
    employer = None
    address = _MockAddressII


MOCK_PERSON_II = {
    "first_name": "Bob",
    "calling_code": 1,
    "phone_number": "(916) 276-6782",
    "employer": None,
    "address": _MOCK_ADDRESS_II,
}


MOCK_PERSON_I_REPR = {
    "name": "Bob",
    "phone": "+1 (916) 276-6782",
    "nested": {"attr": {"deep": "Deep Attribute"}},
    "tags": "mock-person",
    "billing_address": {"city": "Bobtonville", "country": "USA"},
}


MOCK_PERSON_II_REPR = {
    "name": "Bob",
    "phone": "+1 (916) 276-6782",
    "tags": "kwargs-override",
    "billing_address": {"city": "Bobtonville", "country": "MX", "postal_code": "78498"},
}
