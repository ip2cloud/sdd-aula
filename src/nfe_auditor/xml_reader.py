from decimal import Decimal, InvalidOperation
from pathlib import Path

from lxml import etree

from nfe_auditor.domain import Document, Occurrence, ReadOutcome


NAMESPACE = {"nfe": "http://www.portalfiscal.inf.br/nfe"}


def read_xml(path: Path, unreadable_severity: str) -> ReadOutcome:
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        recover=False,
    )
    try:
        root = etree.parse(str(path), parser)
        total_text = root.findtext(".//nfe:ICMSTot/nfe:vNF", namespaces=NAMESPACE)
        product_texts = root.xpath(
            ".//nfe:det/nfe:prod/nfe:vProd/text()", namespaces=NAMESPACE
        )
        if total_text is None or not product_texts:
            raise ValueError("vNF ou vProd ausente")
        document = Document(
            filename=path.name,
            source=path,
            total=Decimal(total_text),
            product_values=tuple(Decimal(text) for text in product_texts),
        )
        return ReadOutcome(document=document, occurrence=None)
    except (OSError, ValueError, InvalidOperation, etree.XMLSyntaxError) as exc:
        occurrence = Occurrence(
            rule_id="xml_unreadable_v1",
            severity=unreadable_severity,
            filename=path.name,
            reason=f"XML ilegível: {exc}",
        )
        return ReadOutcome(document=None, occurrence=occurrence)
