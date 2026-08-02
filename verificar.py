from contextlib import redirect_stdout
from importlib.util import find_spec
import io
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "src"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))


def main() -> int:
    if find_spec("nfe_auditor.runner") is None:
        print("FASE 1 AINDA NÃO IMPLEMENTADA")
        print("Próximo comando: python -m pytest -m aceitacao -v")
        return 0

    from nfe_auditor.config import load_config
    from nfe_auditor.runner import run_audit

    try:
        with TemporaryDirectory() as temporary:
            with redirect_stdout(io.StringIO()):
                result = run_audit(
                    Path("tests/fixtures/xmls"),
                    Path(temporary) / "output",
                    load_config(Path("config.example.toml")),
                )
    except (OSError, ValueError) as exc:
        print("NÃO PASSOU")
        print(f"Falha de execução: {exc}")
        return 1

    rule_occurrences = [
        item
        for item in result.occurrences
        if item.rule_id == "total_note_vs_products_v1"
    ]
    expected_files = {"NFe_0004.xml", "NFe_0038.xml"}
    found_files = {item.filename for item in rule_occurrences}
    false_positive = len(found_files - expected_files)
    print(
        "total_note_vs_products_v1 "
        f"esperado=2 achado={len(rule_occurrences)} "
        f"falso_positivo={false_positive}"
    )
    print(f"notas_sem_divergencia_de_total={50 - len(rule_occurrences)}")
    if found_files == expected_files and false_positive == 0:
        print("FASE PROVADA")
        return 0
    print("NÃO PASSOU")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
