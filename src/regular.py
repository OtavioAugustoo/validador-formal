# Validador de linguagens regulares via autômato finito determinístico (DFA)


def validar(dfa: dict, palavra: str) -> bool:
    """
    Simula um DFA e retorna True se a palavra é aceita.

    dfa = {
        'estados': {...},
        'alfabeto': {...},
        'transicoes': {(estado, simbolo): proximo_estado, ...},
        'estado_inicial': '...',
        'estados_aceitacao': {...}
    }
    """
    estado = dfa['estado_inicial']
    for simbolo in palavra:
        if simbolo not in dfa['alfabeto']:
            return False
        chave = (estado, simbolo)
        if chave not in dfa['transicoes']:
            return False
        estado = dfa['transicoes'][chave]
    return estado in dfa['estados_aceitacao']
