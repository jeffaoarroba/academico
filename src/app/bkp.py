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
