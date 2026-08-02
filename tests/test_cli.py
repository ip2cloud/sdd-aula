from nfe_auditor.cli import build_parser


def test_ajuda_expoe_argumentos_obrigatorios(capsys) -> None:
    parser = build_parser()
    parser.print_help()
    help_text = capsys.readouterr().out
    assert "--input" in help_text
    assert "--output" in help_text
    assert "--config" in help_text
