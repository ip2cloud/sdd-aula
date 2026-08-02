from pathlib import Path

from nfe_auditor.domain import AuditConfig, Counts, Occurrence, RunResult
from nfe_auditor.inventory import inventory_xml
from nfe_auditor.logging import emit_event
from nfe_auditor.report import write_report
from nfe_auditor.rules.contracts import RuleContext
from nfe_auditor.rules.registry import RULES
from nfe_auditor.xml_reader import read_xml


def run_audit(input_dir: Path, output_dir: Path, config: AuditConfig) -> RunResult:
    if input_dir.resolve() == output_dir.resolve():
        raise ValueError("As pastas de entrada e saída devem ser diferentes")

    files = inventory_xml(input_dir)
    documents = []
    occurrences: list[Occurrence] = []
    unreadable = 0

    for path in files:
        outcome = read_xml(path, config.unreadable_severity)
        if outcome.document is None:
            unreadable += 1
            if outcome.occurrence is not None:
                occurrences.append(outcome.occurrence)
            continue
        documents.append(outcome.document)

    for document in documents:
        context = RuleContext(document=document, config=config)
        for rule in RULES:
            occurrences.extend(rule.evaluate(context))

    counts = Counts(
        read=len(files),
        processed=len(documents),
        unreadable=unreadable,
    )
    if not counts.closes():
        raise ValueError("As contagens da execução não fecham")

    report_path = write_report(output_dir, counts, occurrences, config)
    has_blocker = any(
        config.severities[item.severity].blocking for item in occurrences
    )
    exit_code = 1 if has_blocker else 0
    emit_event(
        "execution_completed",
        lidos=counts.read,
        processados=counts.processed,
        ilegíveis=counts.unreadable,
        ocorrências=len(occurrences),
        bloqueantes=sum(
            1
            for item in occurrences
            if config.severities[item.severity].blocking
        ),
        retorno=exit_code,
    )
    return RunResult(
        counts=counts,
        occurrences=tuple(occurrences),
        exit_code=exit_code,
        report_path=report_path,
    )
