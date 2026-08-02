import hashlib
import json
from pathlib import Path


def test_lote_canonico_confere_com_manifesto(fixtures_dir: Path) -> None:
    manifest_path = fixtures_dir.parent / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = sorted(fixtures_dir.glob("*.xml"))
    actual = {
        file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in files
    }

    assert len(files) == 50
    assert len(actual) == 50
    assert actual == manifest["arquivos"]
