from importlib.util import find_spec
from pathlib import Path


def test_scaffold_de_verificacao_existe() -> None:
    assert find_spec("nfe_auditor") is not None
    assert Path("verificar.py").is_file()
