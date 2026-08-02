import json
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from nfe_auditor.config import load_config
from nfe_auditor.rules.contracts import RuleContext
from nfe_auditor.rules.registry import RULES
from nfe_auditor.xml_reader import read_xml


def test_regra_encontra_exatamente_as_duas_divergencias(fixtures_dir: Path) -> None:
    config = load_config(Path("config.example.toml"))
    evaluated: list[str] = []
    occurrences = []
    for path in sorted(fixtures_dir.glob("*.xml")):
        outcome = read_xml(path, config.unreadable_severity)
        assert outcome.document is not None
        evaluated.append(outcome.document.filename)
        occurrences.extend(
            RULES[0].evaluate(RuleContext(outcome.document, config))
        )

    expected = json.loads(
        Path("tests/fixtures/expected_phase1.json").read_text(encoding="utf-8")
    )["rules"]["total_note_vs_products_v1"]
    assert len(evaluated) == 50
    assert len(set(evaluated)) == 50
    assert len(occurrences) == expected["expected"]
    assert [item.filename for item in occurrences] == expected["files"]
    assert [item.value for item in occurrences] == [
        Decimal("-250.00"),
        Decimal("-250.00"),
    ]


def test_regra_detecta_diferenca_positiva_sem_decorar_nome(fixtures_dir: Path) -> None:
    config = load_config(Path("config.example.toml"))
    outcome = read_xml(fixtures_dir / "NFe_0001.xml", config.unreadable_severity)
    assert outcome.document is not None
    total_products = sum(outcome.document.product_values, Decimal("0"))
    changed = replace(outcome.document, total=total_products + Decimal("100.00"))

    occurrences = RULES[0].evaluate(RuleContext(changed, config))
    assert len(occurrences) == 1
    assert occurrences[0].filename == "NFe_0001.xml"
    assert occurrences[0].value == Decimal("100.00")


def test_regra_respeita_tolerancia_pelo_valor_absoluto(fixtures_dir: Path) -> None:
    config = load_config(Path("config.example.toml"))
    outcome = read_xml(fixtures_dir / "NFe_0001.xml", config.unreadable_severity)
    assert outcome.document is not None
    total_products = sum(outcome.document.product_values, Decimal("0"))
    below = replace(outcome.document, total=total_products - Decimal("0.01"))
    above = replace(outcome.document, total=total_products + Decimal("0.01"))
    assert RULES[0].evaluate(RuleContext(below, config)) == ()
    assert RULES[0].evaluate(RuleContext(above, config)) == ()
