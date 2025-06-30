import streamlit as st
from banco import aluno_db
from .aluno_app import AlunoApp

placeholder = st.empty()
aluno_app = AlunoApp(st, placeholder, aluno_db)


class App:
    def __init__(self):
        if "tela" not in st.session_state:
            st.session_state.tela = "listagem"
        if "menu" not in st.session_state:
            st.session_state.menu = "Alunos"

        print("APP", st.session_state.menu.upper(), st.session_state.tela.upper())

        st.sidebar.title("Projeto Academico")
        # o valor selecionado no selectbox vai estar disponivel em st.session_state.menu por causa de key=menu
        st.sidebar.selectbox("Escolha uma opção:", ["Alunos", "Disciplinas", "Matrículas"], key="menu")

        if st.session_state.menu == "Alunos":
            aluno_app.exibir()


__all__ = ["App"]
