import shutil
from pathlib import Path

from nfe_auditor.cli import main
from nfe_auditor.config import load_config
from nfe_auditor.runner import run_audit


def test_retorno_um_com_bloqueante(fixtures_dir: Path, tmp_path: Path) -> None:
    result = run_audit(
        fixtures_dir,
        tmp_path / "output",
        load_config(Path("config.example.toml")),
    )
    assert result.exit_code == 1


def test_retorno_zero_sem_bloqueante(fixtures_dir: Path, tmp_path: Path) -> None:
    clean_input = tmp_path / "input"
    clean_input.mkdir()
    shutil.copy2(fixtures_dir / "NFe_0001.xml", clean_input)
    result = run_audit(
        clean_input,
        tmp_path / "output",
        load_config(Path("config.example.toml")),
    )
    assert result.exit_code == 0


def test_retorno_dois_em_falha_de_execucao(tmp_path: Path) -> None:
    code = main(
        [
            "--input",
            str(tmp_path / "missing"),
            "--output",
            str(tmp_path / "output"),
            "--config",
            "config.example.toml",
        ]
    )
    assert code == 2
