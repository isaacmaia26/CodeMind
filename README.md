# CodeMind

**CodeMind** é um explicador inteligente de código Python.

O utilizador cola ou abre um ficheiro `.py`, e o programa analisa a estrutura interna do código usando `ast` (*Abstract Syntax Tree*) para explicar em linguagem humana o que o script faz.

> Projeto final desenvolvido para demonstrar autonomia, pesquisa e uso de bibliotecas/conceitos além do básico.

---

## Ideia principal

Muitas pessoas aprendem Python, mas têm dificuldade em compreender scripts de outras pessoas. O CodeMind transforma código em explicações claras.

Exemplo:

```python
for i in range(5):
    print(i)
```

O CodeMind interpreta que existe um ciclo `for` e explica que o código repete uma ação várias vezes.

---

## Funcionalidades

- Interface gráfica com `tkinter`
- Análise de código Python com `ast`
- Modo iniciante
- Modo técnico
- Deteção de:
  - funções
  - classes
  - ciclos `for` e `while`
  - condições `if`
  - imports
  - tratamento de erros `try/except`
  - list/dict comprehensions
  - chamadas como `print`, `open`, `eval`, `exec`, `os.system` e `subprocess`
- Score simples de atenção de segurança
- Leitura de ficheiros `.py`
- Voz opcional usando `pyttsx3`

---

## O que foi usado além do básico

### `ast`

O módulo `ast` é nativo do Python e permite transformar código Python numa árvore de sintaxe abstrata. Em vez de apenas procurar palavras no texto, o CodeMind interpreta a estrutura real do código.

### `pyttsx3`

Biblioteca externa opcional usada para transformar a explicação em voz offline.

---

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

Se o `pip` não funcionar no Windows, usa:

```bash
py -m pip install -r requirements.txt
```

### 2. Executar o projeto

```bash
python main.py
```

Ou no Windows:

```bash
py main.py
```

---

## Estrutura do projeto

```text
CodeMind/
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
│
└── codemind/
    ├── __init__.py
    ├── app.py
    ├── explainer.py
    └── speaker.py
```

---

## Exemplo de utilização

1. Abre o programa.
2. Cola código Python na caixa da esquerda.
3. Escolhe entre modo iniciante ou técnico.
4. Clica em **Analisar**.
5. Lê a explicação na caixa da direita.
6. Opcionalmente, clica em **Falar** para ouvir a explicação.

---

## Aviso legal e ético

Este projeto é educativo. Ele não executa nem modifica o código analisado. Apenas interpreta a estrutura do código usando análise estática.

Caso seja usado para analisar scripts de segurança, o objetivo deve ser defensivo, educativo e legal.

---

## Autor

Projeto criado como entrega final das aulas gratuitas de Python.
