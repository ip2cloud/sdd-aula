from importlib.util import find_spec
from pathlib import Path


def test_scaffold_existe_sem_implementar_a_fase_1() -> None:
    assert find_spec("nfe_auditor") is not None
    assert find_spec("nfe_auditor.runner") is None
    assert Path("verificar.py").is_file()
