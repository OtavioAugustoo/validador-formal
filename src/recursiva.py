# reconhecedor da linguagem L = { w#w | w em {0,1}* }
# usa Maquina de Turing deterministica
#
# algoritmo:
#   1. marca o simbolo mais a esquerda nao marcado com X
#   2. atravessa o # e procura o par correspondente na direita
#   3. marca o par com Y e volta pro inicio
#   4. repete ate a esquerda nao ter mais 0 ou 1
#   5. verifica se a direita esta toda marcada com Y tambem
#
# exemplos aceitos:  101#101   0#0   #   (vazia nao ta na linguagem)
# exemplos rejeitados: 101#100   0#1   10#1
#
# Disciplina: Modelagem Computacional

import sys

BRANCO = '_'

# alfabeto de entrada  (# e o separador entre as duas copias)
ALFA_ENTRADA = {'0', '1', '#'}

# alfabeto da fita (inclui os simbolos de marcacao X e Y)
ALFA_FITA = {'0', '1', '#', 'X', 'Y', BRANCO}

ESTADOS = {
    'q0', 'q1', 'q2', 'q3', 'q4',
    'q5', 'q6', 'q7',
    'qaceita', 'qrejeita'
}

# o que cada estado significa:
# q0 - scan da esquerda, procura proximo 0 ou 1 sem marcacao
# q1 - encontrou 0, atravessando pra direita ate o #
# q2 - encontrou 1, atravessando pra direita ate o #
# q3 - passou o #, procura 0 correspondente na direita
# q4 - passou o #, procura 1 correspondente na direita
# q5 - encontrou o par na direita, voltando pra esquerda
# q6 - voltando pelo lado esquerdo ate chegar no inicio
# q7 - esquerda toda marcada, verificando se direita tambem esta

ESTADO_INICIAL    = 'q0'
ESTADOS_ACEITACAO = {'qaceita'}
ESTADOS_REJEICAO  = {'qrejeita'}

# funcao de transicao
# chave: (estado_atual, simbolo_lido)
# valor: (proximo_estado, simbolo_escreve, direcao)   R = direita, L = esquerda
TRANSICOES = {

    # q0: varre a esquerda procurando 0 ou 1 pra marcar
    ('q0', '0'): ('q1', 'X', 'R'),        # marca com X e vai buscar o par
    ('q0', '1'): ('q2', 'X', 'R'),
    ('q0', 'X'): ('q0', 'X', 'R'),        # ja foi marcado, pula
    ('q0', '#'): ('q7', '#', 'R'),        # sem mais 0 ou 1 na esquerda, vai verificar direita
    ('q0', BRANCO): ('qrejeita', BRANCO, 'R'),  # entrada invalida (sem #)

    # q1: achou 0, vai ate o # pra cruzar pro lado direito
    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', 'X'): ('q1', 'X', 'R'),
    ('q1', '#'): ('q3', '#', 'R'),        # cruzou o #, agora procura 0 do outro lado
    ('q1', BRANCO): ('qrejeita', BRANCO, 'R'),  # nao tinha # na entrada

    # q2: achou 1, vai ate o #
    ('q2', '0'): ('q2', '0', 'R'),
    ('q2', '1'): ('q2', '1', 'R'),
    ('q2', 'X'): ('q2', 'X', 'R'),
    ('q2', '#'): ('q4', '#', 'R'),
    ('q2', BRANCO): ('qrejeita', BRANCO, 'R'),

    # q3: na parte direita, procura o 0 correspondente
    ('q3', 'Y'): ('q3', 'Y', 'R'),        # ja casado, pula
    ('q3', '0'): ('q5', 'Y', 'L'),        # achou o par! marca com Y e comeca a voltar
    ('q3', '1'): ('qrejeita', '1', 'R'),  # era pra ser 0 mas achou 1
    ('q3', '#'): ('qrejeita', '#', 'R'),  # segundo # na entrada, invalido
    ('q3', BRANCO): ('qrejeita', BRANCO, 'R'),  # direita acabou sem ter par

    # q4: na parte direita, procura o 1 correspondente
    ('q4', 'Y'): ('q4', 'Y', 'R'),
    ('q4', '1'): ('q5', 'Y', 'L'),
    ('q4', '0'): ('qrejeita', '0', 'R'),  # era pra ser 1 mas achou 0
    ('q4', '#'): ('qrejeita', '#', 'R'),
    ('q4', BRANCO): ('qrejeita', BRANCO, 'R'),

    # q5: par encontrado na direita, voltando pra esquerda
    ('q5', 'Y'): ('q5', 'Y', 'L'),        # passa pelos ja casados voltando
    ('q5', '0'): ('q5', '0', 'L'),
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '#'): ('q6', '#', 'L'),        # cruzou o # voltando

    # q6: passou o # voltando, indo ate o inicio da fita
    ('q6', '0'): ('q6', '0', 'L'),
    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', 'X'): ('q0', 'X', 'R'),        # chegou nos marcados, vira e reinicia o scan

    # q7: verifica se a parte direita esta toda com Y
    ('q7', 'Y'): ('q7', 'Y', 'R'),
    ('q7', BRANCO): ('qaceita', BRANCO, 'R'),  # tudo casado, ACEITA!
    ('q7', '0'): ('qrejeita', '0', 'R'),  # sobrou 0 na direita
    ('q7', '1'): ('qrejeita', '1', 'R'),  # sobrou 1 na direita
}


def fmt_fita(fita, cabeca):
    # mostra a fita ate o ultimo simbolo nao-branco (ou ate a cabeca)
    ultimo = cabeca
    for i in range(len(fita) - 1, -1, -1):
        if fita[i] != BRANCO:
            ultimo = max(ultimo, i)
            break
    partes = []
    for i in range(ultimo + 1):
        cel = fita[i] if i < len(fita) else BRANCO
        partes.append(f'[{cel}]' if i == cabeca else cel)
    return ' '.join(partes)


def validar(cadeia):
    fita   = list(cadeia) + [BRANCO]
    cabeca = 0
    estado = ESTADO_INICIAL
    rastro = []
    passos = 0

    limite = 100_000  # proteção basica contra loop infinito

    for _ in range(limite):
        if estado in ESTADOS_ACEITACAO or estado in ESTADOS_REJEICAO:
            break

        if cabeca >= len(fita):
            fita.append(BRANCO)

        simbolo = fita[cabeca]
        chave   = (estado, simbolo)

        # tira o snapshot da fita antes de escrever
        snap = fmt_fita(fita, cabeca)

        if chave not in TRANSICOES:
            acao = f'transicao ({estado}, {repr(simbolo)}) nao definida'
            rastro.append((estado, cabeca, snap, acao))
            passos += 1
            estado = 'qrejeita'
            break

        prox, escreve, direcao = TRANSICOES[chave]
        acao = f'escreve {repr(escreve)}, move {direcao} -> {prox}'

        fita[cabeca] = escreve
        rastro.append((estado, cabeca, snap, acao))
        passos += 1
        estado = prox

        cabeca += 1 if direcao == 'R' else -1
        cabeca  = max(0, cabeca)

    aceita = estado in ESTADOS_ACEITACAO
    return aceita, passos, rastro


def main():
    if len(sys.argv) < 2:
        print('uso: python src/recursiva.py "<cadeia>"')
        sys.exit(1)

    cadeia = sys.argv[1]
    aceita, passos, rastro = validar(cadeia)

    print(f'Cadeia testada: {cadeia!r}  ({len(cadeia)} simbolos)')
    print(f'Fita inicial:   {" ".join(cadeia) if cadeia else BRANCO}')
    print()
    print('Execucao passo a passo:')
    print(f'  {"#":>5}  {"estado":<10}  {"pos":<4}  {"fita (cel atual entre [ ])":<32}  acao')
    print('  ' + '-' * 80)

    for i, (est, cab, fita_str, acao) in enumerate(rastro, 1):
        print(f'  {i:>5}  {est:<10}  {cab:<4}  {fita_str:<32}  {acao}')

    print()
    print(f'Passos executados: {passos}')
    print(f'Resultado: {"ACEITA" if aceita else "REJEITADA"}')

    sys.exit(0 if aceita else 1)


if __name__ == '__main__':
    main()
