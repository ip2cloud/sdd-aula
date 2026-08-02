from nfe_auditor.rules.registry import RULES


def test_registry_explicito_contem_regra_uma_vez() -> None:
    ids = [rule.rule_id for rule in RULES]
    assert ids == ["total_note_vs_products_v1"]
    assert len(ids) == len(set(ids))
    assert RULES[0].scope == "document"
    assert RULES[0].version == 1
