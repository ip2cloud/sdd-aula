from importlib.util import find_spec


def main() -> int:
    if find_spec("nfe_auditor.runner") is None:
        print("FASE 1 AINDA NÃO IMPLEMENTADA")
        print("Próximo comando: python -m pytest -m aceitacao -v")
        return 0

    print("NÃO PASSOU")
    print("O placar da Fase 1 ainda deve ser implementado em F1-08.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
