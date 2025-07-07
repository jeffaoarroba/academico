# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

## GIT

```bash
# acessar a pasta do projeto no terminal
git add .
git commit -m "resumo da alteracao aqui"
git push (enviar os commits da minha maquina para o servidor git)
```

## PYTHON

o projeto utiliza o python 3.13.3

criar o ambiente virtual (criar a pasta venv) (sem carregar o venv) (so precisa fazer uma vez por novo projeto)

quando voce instala o python, ja vem instalado o modulo/lib venv (nao precisa instalar via comando: `pip install`)

```bash
# acessar a pasta do projeto no terminal
python -m venv .venv
```

precisa sempre ativar o venv (virtual environment) antes de comecar a mecher no projeto e para usar o comando `pip install`

pra carregar o ambiente virtual (a pasta `.venv` pode estar com o nome `venv` tambem) use os comandos abaixo  
> antes de carregar o `venv` o pip nao esta disponivel

# no windows
```cmd
venv\Scripts\activate.bat
# ou
venv\bin\activate.bat
```

# no macOS and Linux
```bash
# acessar a pasta do projeto no terminal
source venv/bin/activate
```

> agora (`venv` carregado) o comando pip estara disponivel

para instalar as libs (e suas dependencias) do projeto (geralmente so precisa rodar uma vez)

```bash
# acessar a pasta do projeto no terminal
pip install -r ./requirements.txt
```

para rodar o streamlite do projeto

```bash
# acessar a pasta do projeto no terminal
# com o venv carregado
streamlit run ./src/app.py
# ou python -m streamlit run ./src/app.py
```

# padroes do projeto

Existe uma convenção oficial para nomeação de arquivos em projetos Python,
e ela está definida na [PEP 8](https://peps.python.org/pep-0008/#package-and-module-names),
que é o guia oficial de estilo para código Python.

> Os módulos devem ter nomes curtos, totalmente em letras minúsculas.  
> Podem ser usados underlines (_) no nome do módulo se isso melhorar a legibilidade.