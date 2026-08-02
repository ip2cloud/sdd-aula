import csv
from pathlib import Path
from typing import Iterable

from nfe_auditor.domain import AuditConfig, Counts, Occurrence, format_decimal


REPORT_NAME = "relatorio.csv"
HEADER = ("tipo", "arquivo", "regra", "severidade", "motivo", "valor")
SUMMARY_ORDER = ("lidos", "processados", "ilegiveis", "bloqueantes", "avisos")


def sort_occurrences(
    occurrences: Iterable[Occurrence], config: AuditConfig
) -> tuple[Occurrence, ...]:
    return tuple(
        sorted(
            occurrences,
            key=lambda item: (
                config.severities[item.severity].rank,
                item.filename,
                item.rule_id,
            ),
        )
    )


def write_report(
    output_dir: Path,
    counts: Counts,
    occurrences: Iterable[Occurrence],
    config: AuditConfig,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / REPORT_NAME
    ordered = sort_occurrences(occurrences, config)
    blockers = sum(
        1 for item in ordered if config.severities[item.severity].blocking
    )
    warnings = len(ordered) - blockers
    summary = {
        "lidos": counts.read,
        "processados": counts.processed,
        "ilegiveis": counts.unreadable,
        "bloqueantes": blockers,
        "avisos": warnings,
    }

    with report_path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination, lineterminator="\n")
        writer.writerow(HEADER)
        for counter in SUMMARY_ORDER:
            writer.writerow(("resumo", "", counter, "", "", summary[counter]))
        for item in ordered:
            value = "" if item.value is None else format_decimal(item.value)
            writer.writerow(
                (
                    "ocorrencia",
                    item.filename,
                    item.rule_id,
                    item.severity,
                    item.reason,
                    value,
                )
            )
    return report_path
