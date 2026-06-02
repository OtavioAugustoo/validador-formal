# Validador de linguagens livres de contexto via autômato de pilha (PDA)


def validar(pda: dict, palavra: str) -> bool:
    """
    Simula um PDA não-determinístico e retorna True se a palavra é aceita
    (por pilha vazia ou por estado de aceitação, conforme configurado em pda['modo']).

    pda = {
        'estado_inicial': '...',
        'simbolo_inicial_pilha': '...',
        'transicoes': {
            (estado, simbolo_entrada_ou_None, topo_pilha): [(proximo_estado, push_pilha), ...]
        },
        'estados_aceitacao': {...},  # usado apenas no modo 'estado'
        'modo': 'estado' | 'pilha_vazia'
    }
    """
    # Configuração: (estado, posição na palavra, pilha)
    configuracoes = {(pda['estado_inicial'], 0, (pda['simbolo_inicial_pilha'],))}
    visitados = set()

    while configuracoes:
        config = configuracoes.pop()
        if config in visitados:
            continue
        visitados.add(config)

        estado, pos, pilha = config

        # Verificar aceitação
        if pos == len(palavra):
            if pda['modo'] == 'pilha_vazia' and len(pilha) == 0:
                return True
            if pda['modo'] == 'estado' and estado in pda['estados_aceitacao']:
                return True

        topo = pilha[-1] if pilha else None

        # Transições com leitura de símbolo
        if pos < len(palavra):
            simbolo = palavra[pos]
            for chave in [(estado, simbolo, topo), (estado, simbolo, None)]:
                for (prox_estado, push) in pda['transicoes'].get(chave, []):
                    nova_pilha = pilha[:-1] + tuple(reversed(push)) if push else pilha[:-1]
                    configuracoes.add((prox_estado, pos + 1, nova_pilha))

        # Transições epsilon
        for chave in [(estado, None, topo), (estado, None, None)]:
            for (prox_estado, push) in pda['transicoes'].get(chave, []):
                nova_pilha = pilha[:-1] + tuple(reversed(push)) if push else pilha[:-1]
                configuracoes.add((prox_estado, pos, nova_pilha))

    return False
