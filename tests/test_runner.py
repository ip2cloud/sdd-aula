from pathlib import Path

from nfe_auditor.config import load_config
from nfe_auditor.runner import run_audit


def test_runner_processa_lote_com_duas_ocorrencias(
    fixtures_dir: Path, tmp_path: Path
) -> None:
    result = run_audit(
        fixtures_dir,
        tmp_path / "output",
        load_config(Path("config.example.toml")),
    )
    assert result.counts.read == 50
    assert result.counts.processed == 50
    assert result.counts.unreadable == 0
    assert len(result.occurrences) == 2
    assert {item.filename for item in result.occurrences} == {
        "NFe_0004.xml",
        "NFe_0038.xml",
    }
    assert result.report_path.name == "relatorio.csv"
