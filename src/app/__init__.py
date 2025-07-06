# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

import streamlit as st
from banco import aluno_db, disciplina_db, matricula_db
from .aluno_app import AlunoApp
from .disciplina_app import DisciplinaApp
from .matricula_app import MatriculaApp


class App:
    def __init__(self):
        if "tela" not in st.session_state:
            st.session_state.tela = "listar_alunos"
        if "menu" not in st.session_state:
            st.session_state.menu = "Alunos"

        print(
            "APP",
            st.session_state.menu.upper(),
            st.session_state.tela.upper()
        )

        st.sidebar.title("Projeto Academico")
        # o valor selecionado no selectbox
        # vai estar disponivel em st.session_state.menu
        # por causa de key=menu
        st.sidebar.selectbox(
            "Escolha uma opção:",
            ["Alunos", "Disciplinas", "Matrículas"],
            key="menu"
        )

        placeholder = st.empty()

        if st.session_state.menu == "Alunos":
            AlunoApp(st, placeholder, aluno_db).exibir()
        elif st.session_state.menu == "Disciplinas":
            DisciplinaApp(st, placeholder, disciplina_db).exibir()
        elif st.session_state.menu == "Matrículas":
            MatriculaApp(st, placeholder, matricula_db,
                         aluno_db, disciplina_db).exibir()


__all__ = ["App"]
