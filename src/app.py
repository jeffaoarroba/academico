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


placeholder = st.empty()

if "tela" not in st.session_state:
    st.session_state.tela = "Lista"

print("INFO", st.session_state.menu, st.session_state.tela)

if st.session_state.menu == "Alunos":
    if st.session_state.tela == "Novo":
        with placeholder.container():
            st.subheader("🧑‍🎓 Aluno | Novo")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            st.button("voltar", on_click=listar_alunos,
                      help="**cancelar** o cadastro do novo aluno e voltar para a listagem de alunos")
            with st.form("novo_aluno"):
                st.write("Informe os dados do novo Aluno")

                cpf = st.text_input("CPF:")
                nome = st.text_input("Nome:", placeholder="nome completo do novo aluno")
                ano_nascimento = st.number_input("Ano de Nascimento:", value=None, min_value=1970,
                                                 max_value=datetime.now().year - 1)
                email = st.text_input("Email:")
                endereco = st.text_input("Endeço:")

                clicou_em_salvar_novo_aluno = st.form_submit_button("salvar novo aluno", icon="💾")

                if clicou_em_salvar_novo_aluno:
                    print("INFO clicou em salvar novo aluno")
                    novoAluno = Aluno(cpf, nome, ano_nascimento, email, endereco)
                    erros = novoAluno.validar()
                    if erros:
                        print("ERRO", erros)
                        for erro in erros:
                            st.error(erro)
                    else:
                        st.success("Aluno salvo com sucesso!")
    else:
        with placeholder.container():
            st.subheader("🧑‍🎓 Aluno | Lista")
            st.button("novo", on_click=novo_aluno, icon="➕")
            alunos = aluno_db.listar_alunos()
            if len(alunos) == 0:
                st.write("nao ha alunos cadastrados")
            else:
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
