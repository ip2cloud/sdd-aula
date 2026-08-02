import argparse
import json
from pathlib import Path
from typing import Sequence

from nfe_auditor.config import ConfigurationError, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nfe-auditor")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        from nfe_auditor.runner import run_audit

        return run_audit(args.input, args.output, config).exit_code
    except (ConfigurationError, OSError, ValueError) as exc:
        print(
            json.dumps(
                {"event": "execution_failed", "reason": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
