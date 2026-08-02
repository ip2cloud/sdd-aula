from pathlib import Path


def inventory_xml(input_dir: Path) -> tuple[Path, ...]:
    if not input_dir.is_dir():
        raise ValueError("A pasta de entrada não existe ou não é uma pasta")
    return tuple(sorted(input_dir.glob("*.xml"), key=lambda path: path.name))
