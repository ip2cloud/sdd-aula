import csv
import json
import shutil
import subprocess
import sys
from decimal import Decimal
from importlib.util import find_spec
from pathlib import Path
from xml.etree import ElementTree

import pytest


RULE_ID = "total_note_vs_products_v1"
EXPECTED_DIVERGENT_FILES = {"NFe_0004.xml", "NFe_0038.xml"}
FIXTURES = Path("tests/fixtures/xmls")
CONFIG = Path("config.example.toml")
NFE_NAMESPACE = {"nfe": "http://www.portalfiscal.inf.br/nfe"}


def _require_phase1() -> None:
    if find_spec("nfe_auditor.runner") is None:
        pytest.skip("Fase 1 ainda não implementada: nfe_auditor.runner não existe")


def _run_auditor(input_dir: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    output_dir.mkdir()
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "nfe_auditor",
            "--input",
            str(input_dir),
            "--output",
            str(output_dir),
            "--config",
            str(CONFIG),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def _assert_program_executed(result: subprocess.CompletedProcess[str]) -> list[dict]:
    evidence = f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    assert "No module named" not in result.stderr, evidence
    try:
        events = [json.loads(line) for line in result.stdout.splitlines() if line]
    except json.JSONDecodeError as exc:
        pytest.fail(f"saída padrão não é JSON válido: {exc}\n{evidence}")
    assert events, f"programa não emitiu log JSON\n{evidence}"
    assert any(event.get("event") == "execution_completed" for event in events), evidence
    assert result.returncode == 1, evidence
    return events


def _rule_files(output_dir: Path) -> list[str]:
    reports = list(output_dir.glob("*.csv"))
    assert len(reports) == 1
    with reports[0].open(encoding="utf-8", newline="") as report:
        rows = csv.DictReader(report)
        return [row["arquivo"] for row in rows if row["regra"] == RULE_ID]


@pytest.mark.aceitacao
def test_encontra_as_duas_divergencias_esperadas(tmp_path: Path) -> None:
    _require_phase1()
    result = _run_auditor(FIXTURES, tmp_path / "output")
    _assert_program_executed(result)
    assert set(_rule_files(tmp_path / "output")) == EXPECTED_DIVERGENT_FILES


@pytest.mark.aceitacao
def test_nao_gera_falso_positivo_da_regra(tmp_path: Path) -> None:
    _require_phase1()
    result = _run_auditor(FIXTURES, tmp_path / "output")
    _assert_program_executed(result)
    files = _rule_files(tmp_path / "output")
    assert len(files) == 2
    assert set(files) == EXPECTED_DIVERGENT_FILES


@pytest.mark.aceitacao
def test_regra_e_generica_e_nao_decora_nome(tmp_path: Path) -> None:
    _require_phase1()
    altered_input = tmp_path / "input"
    shutil.copytree(FIXTURES, altered_input)
    altered_file = altered_input / "NFe_0001.xml"
    tree = ElementTree.parse(altered_file)
    total = tree.find(".//nfe:ICMSTot/nfe:vNF", NFE_NAMESPACE)
    assert total is not None and total.text is not None
    total.text = str(Decimal(total.text) + Decimal("100.00"))
    tree.write(altered_file, encoding="utf-8", xml_declaration=True)

    result = _run_auditor(altered_input, tmp_path / "output")
    _assert_program_executed(result)
    assert set(_rule_files(tmp_path / "output")) == {
        *EXPECTED_DIVERGENT_FILES,
        "NFe_0001.xml",
    }


@pytest.mark.aceitacao
def test_contagens_fecham(tmp_path: Path) -> None:
    _require_phase1()
    result = _run_auditor(FIXTURES, tmp_path / "output")
    events = _assert_program_executed(result)
    summary = next(event for event in events if "lidos" in event)
    assert summary["lidos"] == summary["processados"] + summary["ilegíveis"]
