from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Severity:
    name: str
    blocking: bool
    rank: int


@dataclass(frozen=True, slots=True)
class AuditConfig:
    tolerance: Decimal
    rule_severity: str
    unreadable_severity: str
    severities: Mapping[str, Severity]

    @classmethod
    def create(
        cls,
        *,
        tolerance: Decimal,
        rule_severity: str,
        unreadable_severity: str,
        severities: Mapping[str, Severity],
    ) -> "AuditConfig":
        return cls(
            tolerance=tolerance,
            rule_severity=rule_severity,
            unreadable_severity=unreadable_severity,
            severities=MappingProxyType(dict(severities)),
        )


@dataclass(frozen=True, slots=True)
class Document:
    filename: str
    source: Path
    total: Decimal
    product_values: tuple[Decimal, ...]


@dataclass(frozen=True, slots=True)
class ReadOutcome:
    document: Document | None
    occurrence: "Occurrence | None"


@dataclass(frozen=True, slots=True)
class Occurrence:
    rule_id: str
    severity: str
    filename: str
    reason: str
    value: Decimal | None = None


@dataclass(frozen=True, slots=True)
class Counts:
    read: int
    processed: int
    unreadable: int

    def closes(self) -> bool:
        return self.read == self.processed + self.unreadable


@dataclass(frozen=True, slots=True)
class RunResult:
    counts: Counts
    occurrences: tuple[Occurrence, ...]
    exit_code: int
    report_path: Path


def format_decimal(value: Decimal) -> str:
    return format(value, ".2f")
