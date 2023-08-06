import pytest

from .mocks import (
    MOCK_PERSON_I,
    MOCK_PERSON_I_REPR,
    MOCK_PERSON_II,
    MOCK_PERSON_II_REPR,
    MockPersonI,
    MockPersonII,
)
from .resources import PersonFromMap, PersonFromObj


@pytest.mark.parametrize(
    "mock_person, kwargs, repr",
    [
        (MockPersonI, {}, MOCK_PERSON_I_REPR),
        (
            MockPersonII,
            {"tags": "kwargs-override", "billing_address": {"postal_code": "78498"}},
            MOCK_PERSON_II_REPR,
        ),
    ],
)
def test_from_obj(mock_person, kwargs, repr):
    assert PersonFromObj(mock_person, **kwargs).repr == repr


@pytest.mark.parametrize(
    "mock_person, kwargs, repr",
    [
        (MOCK_PERSON_I, {}, MOCK_PERSON_I_REPR),
        (
            MOCK_PERSON_II,
            {"tags": "kwargs-override", "billing_address": {"postal_code": "78498"}},
            MOCK_PERSON_II_REPR,
        ),
    ],
)
def test_from_map(mock_person, kwargs, repr):
    assert PersonFromMap(mock_person, from_map=True, **kwargs).repr == repr


@pytest.mark.parametrize(
    "mock_person", [MOCK_PERSON_I, MOCK_PERSON_II],
)
def test_from_obj_as_map(mock_person):
    with pytest.raises(TypeError) as exc:
        PersonFromMap(mock_person)

    assert "Sequences are used to fetch nested keys when `from_map` is `True`." in str(
        exc.value
    )
