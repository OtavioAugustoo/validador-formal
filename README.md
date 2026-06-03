# Validador Formal em Três Níveis

Projeto de validação de linguagens formais implementado em Python, cobrindo três níveis da Hierarquia de Chomsky:

- **Linguagens Regulares** — DFA para CPF no formato `ddd.ddd.ddd-dd`
- **Linguagens Livres de Contexto** — PDA para expressões com parênteses, colchetes e chaves balanceados
- **Linguagens Recursivas** — Máquina de Turing para L = { w#w | w ∈ {0,1}* }

Desenvolvido como projeto da disciplina de Modelagem Computacional.

---

## Como rodar

### Todos os testes de uma vez

```
python src/testes.py
```

Lê os casos de `testes/*.txt` e imprime uma tabela comparativa para cada reconhecedor.

### Reconhecedores individuais

```
python src/regular.py "123.456.789-00"
python src/livre_contexto.py "((x+y)*z)"
python src/recursiva.py "101#101"
```

Cada script mostra a execução passo a passo (estado, símbolo lido, ação) e o resultado final.

---

## Estrutura do projeto

```
PROJETO_VALIDADOR/
├── src/
│   ├── regular.py          # DFA — CPF
│   ├── livre_contexto.py   # PDA — parênteses balanceados
│   ├── recursiva.py        # Máquina de Turing — w#w
│   └── testes.py           # bateria de testes
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
└── relatorio/
```
