from decimal import Decimal, InvalidOperation
from pathlib import Path
import tomllib
from typing import Any

from nfe_auditor.domain import AuditConfig, Severity


class ConfigurationError(ValueError):
    pass


def _table(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"Seção obrigatória ausente: {key}")
    return value


def _text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"Valor textual obrigatório inválido: {key}")
    return value


def load_config(path: Path) -> AuditConfig:
    try:
        with path.open("rb") as source:
            data = tomllib.load(source)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"Não foi possível ler a configuração: {exc}") from exc

    rule = _table(_table(data, "rules"), "total_note_vs_products_v1")
    tolerance_text = rule.get("tolerance")
    if not isinstance(tolerance_text, str):
        raise ConfigurationError("A tolerância deve ser uma string decimal")
    try:
        tolerance = Decimal(tolerance_text)
    except InvalidOperation as exc:
        raise ConfigurationError("Tolerância decimal inválida") from exc
    if not tolerance.is_finite() or tolerance < 0:
        raise ConfigurationError("A tolerância deve ser finita e não negativa")

    severities_data = _table(data, "severities")
    severities: dict[str, Severity] = {}
    for name, raw in severities_data.items():
        if not isinstance(raw, dict):
            raise ConfigurationError(f"Severidade inválida: {name}")
        blocking = raw.get("blocking")
        rank = raw.get("rank")
        if not isinstance(blocking, bool):
            raise ConfigurationError(f"Bloqueio inválido para severidade: {name}")
        if isinstance(rank, bool) or not isinstance(rank, int):
            raise ConfigurationError(f"Rank inválido para severidade: {name}")
        severities[name] = Severity(name=name, blocking=blocking, rank=rank)

    rule_severity = _text(rule, "severity")
    xml = _table(data, "xml")
    unreadable_severity = _text(xml, "unreadable_severity")
    for name in (rule_severity, unreadable_severity):
        if name not in severities:
            raise ConfigurationError(f"Severidade não configurada: {name}")

    return AuditConfig.create(
        tolerance=tolerance,
        rule_severity=rule_severity,
        unreadable_severity=unreadable_severity,
        severities=severities,
    )
