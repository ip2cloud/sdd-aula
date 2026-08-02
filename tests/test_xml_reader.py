import hashlib
import json
import shutil
from pathlib import Path

from nfe_auditor.xml_reader import read_xml


def test_le_todo_lote_sem_ilegiveis(fixtures_dir: Path) -> None:
    outcomes = [read_xml(path, "alta") for path in sorted(fixtures_dir.glob("*.xml"))]
    assert len(outcomes) == 50
    assert sum(item.document is not None for item in outcomes) == 50
    assert sum(item.occurrence is not None for item in outcomes) == 0


def test_xml_ilegivel_vira_ocorrencia_e_preserva_originais(
    fixtures_dir: Path, tmp_path: Path
) -> None:
    input_dir = tmp_path / "input"
    shutil.copytree(fixtures_dir, input_dir)
    broken = input_dir / "NFe_0001.xml"
    broken.write_text("<nfeProc>", encoding="utf-8")

    outcomes = [read_xml(path, "alta") for path in sorted(input_dir.glob("*.xml"))]
    assert len(outcomes) == 50
    assert sum(item.document is not None for item in outcomes) == 49
    unreadable = [item.occurrence for item in outcomes if item.occurrence is not None]
    assert len(unreadable) == 1
    assert unreadable[0].filename == "NFe_0001.xml"
    assert unreadable[0].severity == "alta"

    manifest = json.loads(
        (fixtures_dir.parent / "manifest.json").read_text(encoding="utf-8")
    )["arquivos"]
    actual = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in fixtures_dir.glob("*.xml")
    }
    assert actual == manifest
