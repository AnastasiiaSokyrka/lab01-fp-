from core import Policy, make_processor, render_report


def risk_coefficient(risk: float) -> float:
    return 1.0 + risk * 0.5


def discount_policy(
    premium: float,
    experience_years: int,
) -> float:
    if experience_years >= 10:
        discount = 0.20
    elif experience_years >= 5:
        discount = 0.10
    else:
        discount = 0.0

    return premium * (1.0 - discount)


def accept_policy(policy: Policy) -> bool:
    return policy["active"]


def run() -> None:
    policies: list[Policy] = [
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

    processor = make_processor(
        accept=accept_policy,
        risk_coefficient=risk_coefficient,
        discount_policy=discount_policy,
    )

    result = processor(policies)
    print(render_report(result))


if __name__ == "__main__":
    run()
