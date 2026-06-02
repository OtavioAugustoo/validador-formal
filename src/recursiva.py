# Validador de linguagens recursivas via máquina de Turing determinística


BRANCO = '_'


def validar(mt: dict, palavra: str) -> bool:
    """
    Simula uma Máquina de Turing determinística e retorna True se a palavra é aceita.

    mt = {
        'estado_inicial': '...',
        'estados_aceitacao': {...},
        'estados_rejeicao': {...},
        'transicoes': {
            (estado, simbolo): (proximo_estado, novo_simbolo, direcao)  # direcao: 'R' | 'L'
        }
    }
    """
    fita = list(palavra) if palavra else [BRANCO]
    cabeca = 0
    estado = mt['estado_inicial']

    limite = 10_000  # proteção contra loops infinitos em simulações finitas

    for _ in range(limite):
        if estado in mt['estados_aceitacao']:
            return True
        if estado in mt['estados_rejeicao']:
            return False

        simbolo = fita[cabeca] if cabeca < len(fita) else BRANCO
        chave = (estado, simbolo)

        if chave not in mt['transicoes']:
            return False

        estado, novo_simbolo, direcao = mt['transicoes'][chave]

        if cabeca < len(fita):
            fita[cabeca] = novo_simbolo
        else:
            fita.append(novo_simbolo)

        if direcao == 'R':
            cabeca += 1
        elif direcao == 'L':
            cabeca = max(0, cabeca - 1)

    return False  # limite atingido sem aceitação
