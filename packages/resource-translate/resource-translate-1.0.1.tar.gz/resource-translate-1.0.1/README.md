# Resource Translate
Utilities to translate resources between platforms.

[![PyPI](https://img.shields.io/pypi/v/resource-translate.svg)](https://pypi.org/project/resource-translate/)
[![GitHub Actions: CI Workflow](https://github.com/austinbravodev/resource_translate/workflows/CI/badge.svg)](https://github.com/austinbravodev/resource_translate/actions?query=workflow%3ACI)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/austinbravodev/resource_translate/blob/main/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Installation
```shell
pip install resource_translate
```

Or with [testing](#testing):
```shell
pip install resource_translate[dev]
```

---

## Examples

### Translating an Object
Given the following `MockPerson` object:

```python
class _MockAddress:
    town = "Bobtonville"
    country_code = "US"


class MockPerson:
    first_name = "Bob"
    calling_code = 1
    phone_number = "(916) 276-6782"
    employer = None
    address = _MockAddress
```

And the following `PersonFromObj` translator:

```python
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
```

Calling:

```python
PersonFromObj(MockPerson).repr
```

Returns:

```python
{
    "name": "Bob",
    "phone": "+1 (916) 276-6782",
    "nested": {"attr": {"deep": "Deep Attribute"}},
    "tags": "mock-person",
    "billing_address": {"city": "Bobtonville", "country": "USA"},
}
```

### Translating a Mapping
Given the following `MOCK_PERSON` mapping:

```python
_MOCK_ADDRESS = {"town": "Bobtonville", "country_code": "US"}

MOCK_PERSON = {
    "first_name": "Bob",
    "calling_code": 1,
    "phone_number": "(916) 276-6782",
    "employer": None,
    "address": _MOCK_ADDRESS,
}
```

And the following `PersonFromMap` translator:

```python
from resource_translate import Translator, attr


class PersonFromMap(Translator):
    constants = {"tags": "mock-person"}
    mapping = {
        "name": "first_name",
        "billing_address": {"city": ("address", "town")},
        "employer": "employer",
        "missing": "absent",
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
```

Calling:

```python
PersonFromMap(MOCK_PERSON, from_map=True).repr
```

Returns:

```python
{
    "name": "Bob",
    "phone": "+1 (916) 276-6782",
    "nested": {"attr": {"deep": "Deep Attribute"}},
    "tags": "mock-person",
    "billing_address": {"city": "Bobtonville", "country": "USA"},
}
```

### Explicit Attributes

Keyword arguments are set directly on the translated resource - given the prior `PersonFromObj` translator, calling:

```python
PersonFromObj(MockPerson, tags="kwargs-override", billing_address={"postal_code": "78498"}).repr
```

Returns:

```python
{
    "name": "Bob",
    "phone": "+1 (916) 276-6782",
    "nested": {"attr": {"deep": "Deep Attribute"}},
    "tags": "kwargs-override",
    "billing_address": {"city": "Bobtonville", "country": "USA", "postal_code": "78498"},
}
```

For additional examples, see [tests/](tests).

---

## Reference
```shell
$ python
>>> from resource_translate import Translator, attr
>>> help(Translator)
...
>>> help(attr)
...
```

---

## Testing
Having [installed with testing](#installation), invoke [Pytest](https://docs.pytest.org/en/stable/) from the project root:
```shell
pytest
```

Or with coverage:

```shell
pytest --cov src --cov-report term-missing
```