from decimal import Decimal
from pathlib import Path

import pytest

from nfe_auditor.config import ConfigurationError, load_config


def test_carrega_tolerancia_e_severidades_externas() -> None:
    config = load_config(Path("config.example.toml"))
    assert config.tolerance == Decimal("0.01")
    assert config.severities["alta"].blocking is True
    assert config.severities["alta"].rank == 10


@pytest.mark.parametrize(
    "content",
    [
        """
[rules.total_note_vs_products_v1]
severity = "alta"
[xml]
unreadable_severity = "alta"
[severities.alta]
blocking = true
rank = 10
""",
        """
[rules.total_note_vs_products_v1]
tolerance = -0.01
severity = "alta"
[xml]
unreadable_severity = "alta"
[severities.alta]
blocking = true
rank = 10
""",
        """
[rules.total_note_vs_products_v1]
tolerance = "0.01"
severity = "alta"
[xml]
unreadable_severity = "alta"
[severities.alta]
blocking = true
""",
    ],
)
def test_rejeita_configuracao_invalida(tmp_path: Path, content: str) -> None:
    path = tmp_path / "invalid.toml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_config(path)
