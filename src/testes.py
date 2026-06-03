# bateria de testes pros tres reconhecedores
# le os casos de testes/*.txt e mostra uma tabelinha com os resultados
#
# uso:  python src/testes.py
#
# Disciplina: Modelagem Computacional

import sys
import os

# força utf-8 no terminal pra nao ter problema com os simbolos ✓ e ✗ no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# garante que o Python acha os modulos mesmo rodando de outro diretorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from regular        import validar as validar_cpf
from livre_contexto import validar as validar_pilha
from recursiva      import validar as validar_mt

# raiz do projeto fica um nivel acima de src/
RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def ler_casos(caminho):
    # le o arquivo de teste e devolve lista de (cadeia, esperado)
    # formato das linhas: ACEITA <cadeia> ou REJEITA <cadeia>
    casos = []
    with open(caminho, encoding='utf-8') as arq:
        for linha in arq:
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            partes  = linha.split(None, 1)   # divide no primeiro espaco so
            rotulo  = partes[0].upper()
            cadeia  = partes[1] if len(partes) > 1 else ''
            casos.append((cadeia, rotulo == 'ACEITA'))
    return casos


def rodar_bateria(titulo, fn_validar, caminho_teste):
    print()
    print('=' * 65)
    print(f'  {titulo}')
    print('=' * 65)

    casos = ler_casos(caminho_teste)
    if not casos:
        print('  (arquivo vazio ou sem casos validos)')
        return 0, 0

    # descobre a largura necessaria pra coluna cadeia
    largura = max(len(c) if c else len('(vazio)') for c, _ in casos)
    largura = max(largura, 6)

    # cabecalho
    print(f'  {"Cadeia":<{largura}}  {"Esperado":<9}  {"Obtido":<9}  {"Passos":>6}  Status')
    print('  ' + '-' * (largura + 38))

    acertos = 0
    for cadeia, esperado in casos:
        aceita, passos, _ = fn_validar(cadeia)
        correto = aceita == esperado
        if correto:
            acertos += 1

        esp    = 'ACEITA'  if esperado else 'REJEITA'
        obt    = 'ACEITA'  if aceita   else 'REJEITA'
        status = '✓' if correto else '✗'   # ✓ ou ✗
        exibe  = cadeia if cadeia else '(vazio)'

        print(f'  {exibe:<{largura}}  {esp:<9}  {obt:<9}  {passos:>6}  {status}')

    print()
    print(f'  Resultado: {acertos}/{len(casos)} testes passaram')
    return acertos, len(casos)


def main():
    # lista das tres baterias: (titulo, funcao, arquivo)
    baterias = [
        (
            'Linguagem Regular  --  DFA para CPF',
            validar_cpf,
            os.path.join(RAIZ, 'testes', 'testes_regular.txt'),
        ),
        (
            'Linguagem Livre de Contexto  --  PDA para parenteses balanceados',
            validar_pilha,
            os.path.join(RAIZ, 'testes', 'testes_livre_contexto.txt'),
        ),
        (
            'Linguagem Recursiva  --  MT para L = {w#w | w em {0,1}*}',
            validar_mt,
            os.path.join(RAIZ, 'testes', 'testes_recursiva.txt'),
        ),
    ]

    total_acertos = 0
    total_casos   = 0

    for titulo, fn, arq in baterias:
        a, t = rodar_bateria(titulo, fn, arq)
        total_acertos += a
        total_casos   += t

    print()
    print('=' * 65)
    print(f'  TOTAL GERAL: {total_acertos}/{total_casos} testes passaram')
    print('=' * 65)

    sys.exit(0 if total_acertos == total_casos else 1)


if __name__ == '__main__':
    main()
