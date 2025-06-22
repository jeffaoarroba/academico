## GIT

```bash
git add .
git commit -m "resumo da alteracao aqui"
git push (enviar os commits da minha maquina para o servidor git)
```

## PYTHON

criar o ambiente virtual (criar a pasta venv) (sem carregar o venv) (so precisa fazer uma vez por novo projeto)

quando voce instala o python, ja vem instalado o modulo/lib venv (nao precisa instalar via comando: `pip install`)

```bash
python -m venv .venv
```

precisa sempre ativar o venv (virtual environment) antes de comecar a mecher no projeto e para usar o comando `pip install`

pra carregar o ambiente virtual (a pasta `.venv` pode estar com o nome `venv` tambem) use os comandos abaixo  
> antes de carregar o `venv` o pip nao esta disponivel

# no windows
```cmd
venv\Scripts\activate.bat
```

# no macOS and Linux
```bash
source venv/bin/activate
```

a partir desse ponto (`venv` carregado) o comando pip estara disponivel

para instalar as libs (e suas dependencias) do projeto (geralmente so precisa rodar uma vez)

```bash
pip install -r ./requirements.txt
```