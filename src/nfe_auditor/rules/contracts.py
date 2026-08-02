from dataclasses import dataclass
from typing import Callable

from nfe_auditor.domain import AuditConfig, Document, Occurrence


@dataclass(frozen=True, slots=True)
class RuleContext:
    document: Document
    config: AuditConfig


RuleFunction = Callable[[RuleContext], tuple[Occurrence, ...]]


@dataclass(frozen=True, slots=True)
class RuleDefinition:
    rule_id: str
    version: int
    scope: str
    evaluate: RuleFunction
