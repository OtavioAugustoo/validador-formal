# gera os PNG a partir dos arquivos .dot usando graphviz
# uso: python diagramas/gerar_png.py
#
# precisa de:
#   pip install graphviz
#   graphviz instalado no sistema: https://graphviz.org/download/
#
# Disciplina: Modelagem Computacional

import os
import sys

try:
    import graphviz
except ImportError:
    print('Erro: pacote graphviz nao instalado.')
    print('Rode: pip install graphviz')
    sys.exit(1)

PASTA = os.path.dirname(os.path.abspath(__file__))

diagramas = [
    'dfa_regular',
    'pda_livre_contexto',
    'mt_recursiva',
]

print('Gerando PNGs a partir dos .dot...')
erros = 0

for nome in diagramas:
    arq_dot = os.path.join(PASTA, f'{nome}.dot')

    if not os.path.exists(arq_dot):
        print(f'  [ERRO] nao encontrado: {arq_dot}')
        erros += 1
        continue

    try:
        with open(arq_dot, encoding='utf-8') as f:
            fonte = f.read()

        # cria o objeto Source e renderiza como PNG
        # cleanup=True remove o arquivo intermediario que o graphviz escreve
        g = graphviz.Source(fonte, format='png')
        saida = g.render(os.path.join(PASTA, nome), cleanup=True)
        print(f'  ok: {nome}.png')

    except graphviz.backend.ExecutableNotFound:
        print(f'  [ERRO] executavel "dot" nao encontrado no PATH.')
        print('  Instale o Graphviz: https://graphviz.org/download/')
        print('  No Windows com winget: winget install Graphviz.Graphviz')
        erros += 1
        break  # se dot nao existe, nao adianta tentar os outros

    except Exception as e:
        print(f'  [ERRO] {nome}: {e}')
        erros += 1

if erros == 0:
    print('\nProntos! PNG gerados em diagramas/')
else:
    print(f'\n{erros} erro(s). Verifique se o Graphviz esta instalado.')
    sys.exit(1)
