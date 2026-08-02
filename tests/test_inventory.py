from pathlib import Path

import pytest

from nfe_auditor.inventory import inventory_xml


def test_inventario_encontra_50_xmls_em_ordem(fixtures_dir: Path) -> None:
    files = inventory_xml(fixtures_dir)
    assert len(files) == 50
    assert [path.name for path in files] == sorted(path.name for path in files)


def test_inventario_rejeita_pasta_inexistente(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        inventory_xml(tmp_path / "missing")
