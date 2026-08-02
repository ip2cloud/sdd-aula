import ast
from pathlib import Path


def test_codigo_nao_usa_float() -> None:
    violations: list[str] = []
    for root in (Path("src"), Path("tests")):
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and node.id == "float":
                    violations.append(f"{path}:{node.lineno}")
                if isinstance(node, ast.Attribute) and node.attr == "float":
                    violations.append(f"{path}:{node.lineno}")
    assert violations == []
