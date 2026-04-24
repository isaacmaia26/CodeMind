# CodeMind

**CodeMind** é um explicador inteligente de código Python.

O utilizador cola ou abre um ficheiro `.py`, e o programa analisa a estrutura interna do código usando `ast` (*Abstract Syntax Tree*) para explicar em linguagem humana o que o script faz.



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

## O que o CodeMind faz

- Lê código Python
- Analisa a estrutura do código com `ast`
- Explica o código em modo iniciante ou técnico
- Deteta funções, classes, ciclos, condições e imports
- Deteta alguns pontos que merecem atenção, como `eval`, `exec`, `open`, `os.system` e `subprocess`
- Permite abrir ficheiros `.py`
- Tem voz opcional com `pyttsx3`
- Tem interface gráfica feita com `tkinter`


---

## Porque escolhi este projeto

Eu queria fazer algo diferente dos projetos mais comuns, como calculadora, jogo da forca ou lista de tarefas.

A ideia foi criar uma ferramenta que ajudasse uma pessoa a entender código Python. Muitas vezes alguém olha para um script e até sabe algumas coisas, mas não percebe a estrutura geral. O CodeMind tenta resolver isso de uma forma simples.


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
