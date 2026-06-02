# Utilitários para executar baterias de testes nos três validadores


def carregar_casos(caminho: str) -> list[tuple[str, bool]]:
    """
    Lê um arquivo de casos de teste no formato:
        ACEITA palavra
        REJEITA palavra

    Retorna lista de (palavra, esperado_bool).
    """
    casos = []
    with open(caminho, encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            partes = linha.split(maxsplit=1)
            veredicto = partes[0].upper()
            palavra = partes[1] if len(partes) > 1 else ''
            casos.append((palavra, veredicto == 'ACEITA'))
    return casos


def executar_bateria(validar_fn, automato: dict, casos: list[tuple[str, bool]]) -> dict:
    """
    Executa a função validar_fn para cada caso e compara com o resultado esperado.
    Retorna um dict com: total, corretos, erros (lista de detalhes).
    """
    erros = []
    corretos = 0
    for palavra, esperado in casos:
        obtido = validar_fn(automato, palavra)
        if obtido == esperado:
            corretos += 1
        else:
            erros.append({
                'palavra': repr(palavra),
                'esperado': esperado,
                'obtido': obtido,
            })
    return {'total': len(casos), 'corretos': corretos, 'erros': erros}


def imprimir_resultado(resultado: dict, nome: str = '') -> None:
    titulo = f"=== {nome} ===" if nome else "=== Resultado ==="
    print(titulo)
    print(f"  Total   : {resultado['total']}")
    print(f"  Corretos: {resultado['corretos']}")
    print(f"  Erros   : {len(resultado['erros'])}")
    for e in resultado['erros']:
        print(f"    palavra={e['palavra']}  esperado={e['esperado']}  obtido={e['obtido']}")
    print()
