import json
from pathlib import Path

from nfe_auditor.config import load_config
from nfe_auditor.runner import run_audit


def test_log_e_json_com_contagens(
    fixtures_dir: Path, tmp_path: Path, capsys
) -> None:
    run_audit(
        fixtures_dir,
        tmp_path / "output",
        load_config(Path("config.example.toml")),
    )
    lines = capsys.readouterr().out.splitlines()
    events = [json.loads(line) for line in lines]
    assert events == [
        {
            "bloqueantes": 2,
            "event": "execution_completed",
            "ilegíveis": 0,
            "lidos": 50,
            "ocorrências": 2,
            "processados": 50,
            "retorno": 1,
        }
    ]
