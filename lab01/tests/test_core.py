from copy import deepcopy

from core import (
    Policy,
    compose,
    make_multiplier,
    make_processor,
)


def sample_policies() -> list[Policy]:
    return [
        {
            "id": 1,
            "base_premium": 1000.0,
            "risk": 1.0,
            "experience_years": 5,
            "active": True,
        },
        {
            "id": 2,
            "base_premium": 1500.0,
            "risk": 0.5,
            "experience_years": 12,
            "active": True,
        },
        {
            "id": 3,
            "base_premium": 800.0,
            "risk": 0.2,
            "experience_years": 2,
            "active": False,
        },
    ]


def default_processor():
    return make_processor(
        accept=lambda policy: policy["active"],
        risk_coefficient=lambda risk: 1.0 + risk * 0.5,
        discount_policy=lambda premium, years: premium
        * (1.0 - (0.20 if years >= 10 else 0.10 if years >= 5 else 0.0)),
    )


def test_referential_transparency():
    policies = sample_policies()
    processor = default_processor()

    result1 = processor(policies)
    result2 = processor(policies)

    assert result1 == result2


def test_no_mutation():
    policies = sample_policies()
    original = deepcopy(policies)

    default_processor()(policies)

    assert policies == original


def test_callable_policies():
    policies = sample_policies()

    processor = make_processor(
        accept=lambda policy: policy["active"],
        risk_coefficient=lambda risk: 1.0 + risk,
        discount_policy=lambda premium, years: premium * 0.9,
    )

    result = processor(policies)

    assert result["count"] == 2
    assert result["policies"][0]["final_premium"] == 1800.0
    assert result["revenue"] == 3825.0


def test_inactive_policies_are_skipped():
    policies = sample_policies()
    result = default_processor()(policies)

    assert result["count"] == 2
    assert all(policy["active"] for policy in result["policies"])


def test_compose():
    add_one = lambda x: x + 1
    double = lambda x: x * 2

    combined = compose(add_one, double)

    assert combined(3) == 7


def test_make_multiplier():
    triple = make_multiplier(3)

    assert triple(4) == 12
