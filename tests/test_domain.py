from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree

from nfe_auditor.domain import Counts, format_decimal


NAMESPACE = {"nfe": "http://www.portalfiscal.inf.br/nfe"}


def test_valores_do_lote_podem_ser_lidos_como_decimal(fixtures_dir: Path) -> None:
    values = []
    for path in sorted(fixtures_dir.glob("*.xml")):
        root = ElementTree.parse(path).getroot()
        nodes = root.findall(".//nfe:det/nfe:prod/nfe:vProd", NAMESPACE)
        total = root.find(".//nfe:ICMSTot/nfe:vNF", NAMESPACE)
        assert total is not None and total.text is not None
        values.extend(Decimal(node.text) for node in nodes if node.text is not None)
        values.append(Decimal(total.text))

    assert len(list(fixtures_dir.glob("*.xml"))) == 50
    assert values
    assert all(isinstance(value, Decimal) for value in values)


def test_contagens_fecham() -> None:
    assert Counts(read=50, processed=49, unreadable=1).closes()
    assert not Counts(read=50, processed=48, unreadable=1).closes()


def test_formatacao_decimal_e_independente_de_localizacao() -> None:
    assert format_decimal(Decimal("-250")) == "-250.00"
    assert format_decimal(Decimal("1234.5")) == "1234.50"
