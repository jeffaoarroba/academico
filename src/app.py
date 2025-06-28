import streamlit as st

from datetime import datetime
from banco import aluno_db
from tipos.aluno import Aluno

clicou_em_salvar_novo_aluno = None

placeholder = st.empty()

if 'view' not in st.session_state:
    st.session_state.view = "mostrar_alunos"


def novo_aluno():
    st.session_state.view = "novo_aluno"


def mostrar_alunos():
    st.session_state.view = "mostrar_alunos"


def mostrar_disciplinas():
    st.session_state.view = "mostrar_disciplinas"


def mostrar_matriculas():
    st.session_state.view = "mostrar_matriculas"


if st.session_state.view == "novo_aluno":
    with placeholder.container():
        st.subheader("🧑‍🎓 Aluno | Novo")
        st.button("voltar", on_click=mostrar_alunos)
        with st.form("novo_aluno"):
            st.write("Informe os dados do novo Aluno")

            cpf = st.text_input("CPF:")
            nome = st.text_input("Nome:", placeholder="nome completo do novo aluno")
            ano_nascimento = st.number_input("Ano de Nascimento:", value=None, min_value=1970,
                                            max_value=datetime.now().year - 1)
            email = st.text_input("Email:")
            endereco = st.text_input("Endeço:")

            clicou_em_salvar_novo_aluno = st.form_submit_button("salvar novo aluno", icon="💾")


if st.session_state.view == "mostrar_alunos":
    with placeholder.container():
        st.subheader("🧑‍🎓 Aluno | Lista")
        st.button("novo", on_click=novo_aluno, icon="➕")
        alunos = aluno_db.listar_alunos()
        if len(alunos) == 0:
            st.write("nao ha alunos cadastrados")
        else:
            st.dataframe(alunos)

if st.session_state.view == "mostrar_disciplinas":
    with placeholder.container():
        st.subheader("Lista de Disciplinas")
        st.dataframe([
            {"Código": 1, "Nome": "Matemática", "Carga Horária": 60},
            {"Código": 2, "Nome": "Português", "Carga Horária": 45}
        ])

if st.session_state.view == "mostrar_matriculas":
    with placeholder.container():
        st.subheader("Lista de Matrículas")
        st.dataframe([
            {"Aluno CPF": "123", "Disciplina": "Matemática", "Data": "2025-01-10"},
            {"Aluno CPF": "456", "Disciplina": "Português", "Data": "2025-01-12"}
        ])

st.sidebar.title("Projeto Academico")
opcao = st.sidebar.radio("Escolha uma opção:", ["🧑‍🎓 Alunos", "Disciplinas", "Matrículas"])

# Mostrar conteúdo conforme opção
if opcao == "🧑‍🎓 Alunos":
    mostrar_alunos()
elif opcao == "Disciplinas":
    mostrar_disciplinas()
elif opcao == "Matrículas":
    mostrar_matriculas()

# st.write("Jefferson | Projeto Academico")

if clicou_em_salvar_novo_aluno:
    print("CLICOU EM salvar novo aluno")
    novoAluno = Aluno(cpf, nome, ano_nascimento, email, endereco)
    erros = novoAluno.validar()
    print("ERRO ao salvar novo aluno", erros)
    if erros:
        for erro in erros:
            st.error(erro)
    else:
        st.success("Aluno salvo com sucesso!")
