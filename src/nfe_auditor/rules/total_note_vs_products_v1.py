from decimal import Decimal

from nfe_auditor.domain import Occurrence, format_decimal
from nfe_auditor.rules.contracts import RuleContext


RULE_ID = "total_note_vs_products_v1"


def evaluate(context: RuleContext) -> tuple[Occurrence, ...]:
    total_products = sum(context.document.product_values, Decimal("0"))
    difference = context.document.total - total_products
    if abs(difference) <= context.config.tolerance:
        return ()

    total_text = format_decimal(context.document.total)
    products_text = format_decimal(total_products)
    difference_text = format_decimal(difference)
    tolerance_text = format_decimal(context.config.tolerance)
    reason = (
        f"Total da nota {total_text} difere da soma dos produtos "
        f"{products_text} em {difference_text}; tolerância {tolerance_text}."
    )
    return (
        Occurrence(
            rule_id=RULE_ID,
            severity=context.config.rule_severity,
            filename=context.document.filename,
            reason=reason,
            value=difference,
        ),
    )
