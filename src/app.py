import pandas as pd
import streamlit as st
from datetime import datetime
from banco import aluno_db
from tipos.aluno import Aluno

st.sidebar.title("Projeto Academico")

# o valor selecionado no selectbox vai estar disponivel em st.session_state.menu por causa de key=menu
st.sidebar.selectbox("Escolha uma opção:", ["Alunos", "Disciplinas", "Matrículas"], key="menu")


def listar_alunos():
    st.session_state.menu = "Alunos"
    st.session_state.tela = "Lista"


def novo_aluno():
    st.session_state.menu = "Alunos"
    st.session_state.tela = "Novo"


def salvar_novo_aluno():
    print("INFO clicou em salvar novo aluno")
    novo_aluno = Aluno(
        st.session_state.novo_aluno_cpf,
        st.session_state.novo_aluno_nome.upper(),
        st.session_state.novo_aluno_ano,
        st.session_state.novo_aluno_email.upper(),
        st.session_state.novo_aluno_endereco.upper())
    erros = novo_aluno.validar()
    if erros:
        print("ERRO", erros)
        st.error("⚠️ Revise as informações e tente novamente")
        for erro in erros:
            st.error(erro)
    else:
        aluno_db.cadastrar(novo_aluno)
        st.session_state.tela = "novo_aluno_sucesso"


placeholder = st.empty()

if "tela" not in st.session_state:
    st.session_state.tela = "Lista"

print("INFO", st.session_state.menu, st.session_state.tela)

if st.session_state.menu == "Alunos":
    if st.session_state.tela == "novo_aluno_sucesso" and "novo_aluno_nome" in st.session_state:
        st.subheader("🧑‍🎓 Aluno")
        st.success("Aluno salvo com sucesso!")
        st.write("🧑", st.session_state.novo_aluno_nome.upper())
        st.write("🪪", st.session_state.novo_aluno_cpf)
        st.write("🗓️", st.session_state.novo_aluno_ano)
        st.write("✉️", st.session_state.novo_aluno_email.upper())
        st.write("🛣️", st.session_state.novo_aluno_endereco.upper())
        st.button("voltar", on_click=listar_alunos, help="voltar para a listagem de alunos")
    elif st.session_state.tela == "Novo":
        with placeholder.container():
            st.subheader("🧑‍🎓 Aluno | Novo")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            st.button("voltar", on_click=listar_alunos,
                      help="**cancelar** o cadastro do novo aluno e voltar para a listagem de alunos")
            with st.form("novo_aluno"):
                st.write("Informe os dados do novo Aluno")

                cpf = st.text_input("CPF:", max_chars=11, placeholder="informe somente os numeros do CPF", icon="🪪",
                                    key="novo_aluno_cpf")
                nome = st.text_input("Nome:", max_chars=200, placeholder="informe o nome completo do novo aluno",
                                     icon="🧑", key="novo_aluno_nome")
                ano_nascimento = st.number_input("Ano de Nascimento:", value=None, min_value=1970,
                                                 max_value=datetime.now().year - 1,
                                                 help="se a data de nascimento do Aluno é 01/02/2003, informe somente o ano 2003",
                                                 placeholder="informe somente o ANO da data de nascimento do Aluno",
                                                 icon="🗓️", key="novo_aluno_ano")
                email = st.text_input("Email:", max_chars=200, icon="✉️", key="novo_aluno_email")
                endereco = st.text_input("Endeço:", max_chars=200, icon="🛣️", key="novo_aluno_endereco")

                st.form_submit_button("salvar novo aluno", icon="💾", on_click=salvar_novo_aluno)

    else:
        with placeholder.container():
            st.subheader("🧑‍🎓 Aluno | Lista")
            st.button("novo aluno", on_click=novo_aluno, icon="➕")
            alunos = aluno_db.listar()
            if len(alunos) == 0:
                st.write("nao ha alunos cadastrados")
            else:
                # aluno_com_colunas = pd.DataFrame(alunos, columns=["CPF", "Aluno", "Endereco"])
                st.dataframe(alunos)

if st.session_state.menu == "Disciplinas":
    with placeholder.container():
        st.subheader("Lista de Disciplinas")
        st.dataframe([
            {"Código": 1, "Nome": "Matemática", "Carga Horária": 60},
            {"Código": 2, "Nome": "Português", "Carga Horária": 45}
        ])

if st.session_state.menu == "Matrículas":
    with placeholder.container():
        st.subheader("Lista de Matrículas")
        st.dataframe([
            {"Aluno CPF": "123", "Disciplina": "Matemática", "Data": "2025-01-10"},
            {"Aluno CPF": "456", "Disciplina": "Português", "Data": "2025-01-12"}
        ])

# st.write("Jefferson | Projeto Academico")

### debug
# para ver as variaveis globais do streamlit
# st.write(st.session_state)
