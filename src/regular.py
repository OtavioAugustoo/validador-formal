# validador de CPF usando DFA (automato finito deterministico)
# formato aceito: ddd.ddd.ddd-dd
#
# cada estado representa quantos simbolos corretos ja foram lidos
# q0 = inicio, q14 = unico estado de aceitacao, qerro = estado morto
#
# Disciplina: Modelagem Computacional

import sys

# todos os digitos possiveis
DIGITOS = set('0123456789')

# conjunto de todos os estados do automato
ESTADOS = {
    'q0', 'q1', 'q2', 'q3',
    'q4', 'q5', 'q6', 'q7',
    'q8', 'q9', 'q10', 'q11',
    'q12', 'q13', 'q14',
    'qerro'
}

# simbolos que o automato reconhece
ALFABETO = DIGITOS | {'.', '-'}

ESTADO_INICIAL = 'q0'

# so tem um estado final
ESTADOS_FINAIS = {'q14'}

# tabela de transicao compacta
# usei 'd' no lugar de cada digito pra nao repetir 10 vezes a mesma linha
# a funcao expandir_tabela() resolve isso depois
TABELA_TRANSICOES = {
    ('q0',  'd'): 'q1',    # 1o digito
    ('q1',  'd'): 'q2',    # 2o digito
    ('q2',  'd'): 'q3',    # 3o digito - fim do primeiro grupo
    ('q3',  '.'): 'q4',    # ponto separador
    ('q4',  'd'): 'q5',
    ('q5',  'd'): 'q6',
    ('q6',  'd'): 'q7',    # fim do segundo grupo
    ('q7',  '.'): 'q8',    # segundo ponto
    ('q8',  'd'): 'q9',
    ('q9',  'd'): 'q10',
    ('q10', 'd'): 'q11',   # fim do terceiro grupo
    ('q11', '-'): 'q12',   # hifen
    ('q12', 'd'): 'q13',   # 1o digito verificador
    ('q13', 'd'): 'q14',   # 2o digito verificador -> ACEITA
    # q14 nao tem transicao definida, entao qualquer coisa depois vai pra qerro
}


def expandir_tabela(tabela):
    # substitui o 'd' pelos 10 digitos reais (0-9)
    resultado = {}
    for (estado, s), destino in tabela.items():
        if s == 'd':
            for d in DIGITOS:
                resultado[(estado, d)] = destino
        else:
            resultado[(estado, s)] = destino
    return resultado


TRANSICOES = expandir_tabela(TABELA_TRANSICOES)


def validar(cadeia):
    estado = ESTADO_INICIAL
    rastro = []
    passos = 0

    for simbolo in cadeia:
        # busca a transicao, se nao achar vai pro estado de erro
        proximo = TRANSICOES.get((estado, simbolo), 'qerro')

        rastro.append((estado, simbolo, proximo))
        passos += 1
        estado = proximo

        # chegou no estado morto, nao tem mais o que fazer
        if estado == 'qerro':
            break

    aceita = estado in ESTADOS_FINAIS
    return aceita, passos, rastro


def main():
    if len(sys.argv) < 2:
        print('uso: python src/regular.py "<cpf>"')
        sys.exit(1)

    cadeia = sys.argv[1]
    aceita, passos, rastro = validar(cadeia)

    print(f'Cadeia testada: {cadeia!r}  ({len(cadeia)} simbolos)')
    print()
    print('Execucao passo a passo:')
    print(f'  {"passo":>5}  {"estado atual":<10}  simbolo  proximo estado')
    print('  ' + '-' * 42)

    for i, (atual, simbolo, proximo) in enumerate(rastro, 1):
        # marca o estado final com uma seta
        marca = '  <-- ACEITA' if proximo in ESTADOS_FINAIS else ''
        print(f'  {i:>5}  {atual:<10}  {repr(simbolo):^7}  {proximo}{marca}')

    print()
    print(f'Passos executados: {passos}')
    print(f'Resultado: {"ACEITA" if aceita else "REJEITADA"}')

    sys.exit(0 if aceita else 1)


if __name__ == '__main__':
    main()
