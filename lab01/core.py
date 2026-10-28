from collections.abc import Callable
from typing import TypedDict, TypeVar


class Policy(TypedDict):
    id: int
    base_premium: float
    risk: float
    experience_years: int
    active: bool


class ProcessedPolicy(Policy):
    final_premium: float


class PolicyResult(TypedDict):
    count: int
    revenue: float
    policies: list[ProcessedPolicy]


RiskFn = Callable[[float], float]
DiscountFn = Callable[[float, int], float]
FilterFn = Callable[[Policy], bool]

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def get_base_premium(policy: Policy) -> float:
    return policy["base_premium"]


def calculate_risk_premium(
    base_premium: float,
    risk: float,
    risk_coefficient: RiskFn,
) -> float:
    return base_premium * risk_coefficient(risk)


def apply_experience_discount(
    premium: float,
    experience_years: int,
    discount_policy: DiscountFn,
) -> float:
    return discount_policy(premium, experience_years)


def calculate_final_premium(
    policy: Policy,
    risk_coefficient: RiskFn,
    discount_policy: DiscountFn,
) -> float:
    base = get_base_premium(policy)
    adjusted = calculate_risk_premium(
        base,
        policy["risk"],
        risk_coefficient,
    )
    return apply_experience_discount(
        adjusted,
        policy["experience_years"],
        discount_policy,
    )


def with_final_premium(
    policy: Policy,
    premium: float,
) -> ProcessedPolicy:
    return {**policy, "final_premium": premium}


def make_processor(
    *,
    accept: FilterFn,
    risk_coefficient: RiskFn,
    discount_policy: DiscountFn,
) -> Callable[[list[Policy]], PolicyResult]:

    def process(policies: list[Policy]) -> PolicyResult:
        qualified: list[ProcessedPolicy] = []

        for policy in policies:
            if not accept(policy):
                continue

            premium = calculate_final_premium(
                policy,
                risk_coefficient,
                discount_policy,
            )

            qualified.append(with_final_premium(policy, premium))

        return {
            "count": len(qualified),
            "revenue": sum(policy["final_premium"] for policy in qualified),
            "policies": qualified,
        }

    return process


def compose(
    f: Callable[[B], C],
    g: Callable[[A], B],
) -> Callable[[A], C]:
    return lambda x: f(g(x))


def make_multiplier(k: int) -> Callable[[int], int]:
    return lambda x: x * k


def render_report(result: PolicyResult) -> str:
    lines = ["Insurance policy report"]

    for policy in result["policies"]:
        lines.append(f"Policy {policy['id']}: " f"{policy['final_premium']:.2f} UAH")

    lines.append(f"Active policies processed: {result['count']}")
    lines.append(f"Total premiums: {result['revenue']:.2f} UAH")

    return "\n".join(lines)
