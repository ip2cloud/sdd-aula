from nfe_auditor.rules.contracts import RuleDefinition
from nfe_auditor.rules.total_note_vs_products_v1 import RULE_ID, evaluate


RULES = (
    RuleDefinition(
        rule_id=RULE_ID,
        version=1,
        scope="document",
        evaluate=evaluate,
    ),
)
