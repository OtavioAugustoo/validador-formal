# validador de expressoes com parenteses, colchetes e chaves balanceados
# reconhecedor: PDA (automato de pilha)
#
# letras, numeros e operadores sao ignorados, so os agrupadores importam
# aceitacao por estado final: chega em qf quando acaba a entrada e pilha so tem Z
#
# Disciplina: Modelagem Computacional

import sys

# --- definicao do PDA ---

ESTADOS = {'q0', 'qf', 'qerro'}

# separei os simbolos de abertura e fechamento pra facilitar
ABRE  = {'(', '[', '{'}
FECHA = {')', ']', '}'}

# qual abertura cada fechamento espera encontrar no topo
PAR = {')': '(', ']': '[', '}': '{'}

# alfabeto da pilha  (Z e o marcador de fundo, nunca sai da pilha normalmente)
ALFA_PILHA = {'Z', '(', '[', '{'}

ESTADO_INICIAL = 'q0'
FUNDO          = 'Z'
ESTADOS_FINAIS = {'qf'}

# tabela de transicoes do PDA
# formato: (estado, simbolo_lido, topo_pilha) -> (proximo_estado, push)
#
# push = lista que substitui o topo apos a transicao
# push[0] vai pro topo, push[1] fica abaixo, e assim por diante
#
# obs: simbolos que nao sao colchete/parentese/chave nao aparecem aqui
# o simulador simplesmente ignora eles (nao muda pilha nem estado)

TRANSICOES = {}

# para qualquer simbolo de abertura: empilha em cima do que ja tem
for ab in ABRE:
    for topo in ALFA_PILHA:
        TRANSICOES[('q0', ab, topo)] = ('q0', [ab, topo])

# para fechamento: verifica se bate com o topo
# se sim desempilha, se nao vai pro erro
for fe, ab in PAR.items():
    for topo in ALFA_PILHA:
        if topo == ab:
            TRANSICOES[('q0', fe, topo)] = ('q0', [])           # topo correto, desempilha
        else:
            TRANSICOES[('q0', fe, topo)] = ('qerro', [topo])    # mismatch, erro

# epsilon no final: se so tem Z na pilha entao esta tudo balanceado
TRANSICOES[('q0', None, FUNDO)] = ('qf', [FUNDO])


# --- simulador ---

def descrever(simbolo, topo, prox):
    # monta a descricao da acao pra mostrar no passo a passo
    if prox == 'qerro':
        if topo == FUNDO:
            return f'ERRO: fecha {simbolo!r} com pilha vazia'
        return f'ERRO: fecha {simbolo!r}, topo e {topo!r}'
    if simbolo in ABRE:
        return f'empilha {simbolo!r}'
    if simbolo in FECHA:
        return f'desempilha {topo!r}'
    if simbolo is None:
        return 'epsilon: pilha OK, aceita'
    return f'ignora {simbolo!r}'


def validar(cadeia):
    estado = ESTADO_INICIAL
    pilha  = [FUNDO]
    rastro = []
    passos = 0

    for simbolo in cadeia:
        topo  = pilha[-1]
        chave = (estado, simbolo, topo)

        if chave in TRANSICOES:
            prox, push = TRANSICOES[chave]
            pilha.pop()
            # push[0] tem que ficar no topo, por isso estende ao contrario
            pilha.extend(reversed(push))
        else:
            # nao e colchete/parentese/chave, so passa
            prox = estado

        acao = descrever(simbolo, topo, prox)
        rastro.append((estado, topo, simbolo, acao, list(pilha)))
        passos += 1
        estado = prox

        if estado == 'qerro':
            break

    # terminou a entrada, verifica transicao epsilon
    if estado == 'q0' and pilha:
        topo  = pilha[-1]
        chave = ('q0', None, topo)
        if chave in TRANSICOES:
            prox, push = TRANSICOES[chave]
            acao = descrever(None, topo, prox)
            pilha.pop()
            pilha.extend(reversed(push))
            rastro.append((estado, topo, '(eps)', acao, list(pilha)))
            passos += 1
            estado = prox

    aceita = estado in ESTADOS_FINAIS
    return aceita, passos, rastro


def main():
    if len(sys.argv) < 2:
        print('uso: python src/livre_contexto.py "<expressao>"')
        sys.exit(1)

    cadeia = sys.argv[1]
    aceita, passos, rastro = validar(cadeia)

    print(f'Cadeia testada: {cadeia!r}  ({len(cadeia)} simbolos)')
    print(f'Pilha inicial: [{FUNDO}]  (Z = marcador de fundo)')
    print()
    print('Execucao passo a passo:')
    print(f'  {"#":>4}  {"estado":<7}  {"topo":<5}  {"simbolo":<7}  {"acao":<38}  pilha apos')
    print('  ' + '-' * 78)

    for i, (est, topo, simb, acao, p) in enumerate(rastro, 1):
        print(f'  {i:>4}  {est:<7}  {topo:<5}  {repr(simb):<7}  {acao:<38}  {p}')

    print()
    print(f'Passos executados: {passos}')
    print(f'Resultado: {"ACEITA" if aceita else "REJEITADA"}')

    sys.exit(0 if aceita else 1)


if __name__ == '__main__':
    main()
