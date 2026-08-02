from decimal import Decimal
from pathlib import Path

from nfe_auditor.config import load_config
from nfe_auditor.domain import Counts, Occurrence
from nfe_auditor.report import write_report


def test_relatorio_e_identico_ao_esperado(tmp_path: Path) -> None:
    config = load_config(Path("config.example.toml"))
    occurrences = (
        Occurrence(
            rule_id="total_note_vs_products_v1",
            severity="alta",
            filename="NFe_0038.xml",
            reason=(
                "Total da nota -104.80 difere da soma dos produtos 145.20 "
                "em -250.00; tolerância 0.01."
            ),
            value=Decimal("-250.00"),
        ),
        Occurrence(
            rule_id="total_note_vs_products_v1",
            severity="alta",
            filename="NFe_0004.xml",
            reason=(
                "Total da nota 876.25 difere da soma dos produtos 1126.25 "
                "em -250.00; tolerância 0.01."
            ),
            value=Decimal("-250.00"),
        ),
    )
    report = write_report(
        tmp_path / "output",
        Counts(read=50, processed=50, unreadable=0),
        occurrences,
        config,
    )
    expected = Path("tests/fixtures/expected_report_phase1.csv").read_bytes()
    assert report.name == "relatorio.csv"
    assert report.read_bytes() == expected
    assert list(tmp_path.rglob("*.csv")) == [report]


def test_caminhos_diferentes_geram_bytes_iguais(tmp_path: Path) -> None:
    config = load_config(Path("config.example.toml"))
    occurrence = Occurrence(
        rule_id="rule",
        severity="aviso",
        filename="nota.xml",
        reason="Aviso sem valor natural.",
    )
    counts = Counts(read=1, processed=1, unreadable=0)
    first = write_report(tmp_path / "one", counts, (occurrence,), config)
    second = write_report(tmp_path / "two", counts, (occurrence,), config)
    assert first.read_bytes() == second.read_bytes()
