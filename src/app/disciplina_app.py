# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

from banco.disciplina_db import DisciplinaDB
from tipo.disciplina import Disciplina


class DisciplinaApp:

    def __init__(self, st, placeholder, disciplina_db: DisciplinaDB):
        self.st = st
        self.placeholder = placeholder
        self.disciplina_db = disciplina_db

        if not "excluir_disciplina_erro" in self.st.session_state:
            self.st.session_state.excluir_disciplina_erro = None
        if not "excluir_disciplina_mensagem" in self.st.session_state:
            self.st.session_state.excluir_disciplina_mensagem = None
        if not "editar_disciplina_erro" in self.st.session_state:
            self.st.session_state.editar_disciplina_erro = None

        # debug de variaveis de sessao
        self.st.write(self.st.session_state)

    # NOVA DISCIPLINA

    def obter_nova_disciplina(self):
        return Disciplina(
            self.st.session_state.nova_disciplina_nome,
            self.st.session_state.nova_disciplina_carga_horaria,
            self.st.session_state.nova_disciplina_professor,
        )

    def nova_disciplina_salvar(self):
        print("APP DISCIPLINA clicou em salvar nova disciplina")

        nova_disciplina = self.obter_nova_disciplina()

        erros = nova_disciplina.validar()

        # TODO validar se jah existe uma disciplina cadastrada com o mesmo nome
        self.st.session_state.erros = erros

        if not erros:
            disciplina_codigo = self.disciplina_db.cadastrar(nova_disciplina)
            self.st.session_state.nova_disciplina_codigo = disciplina_codigo
            self.st.session_state.tela = "nova_disciplina_sucesso"

    # EDITAR DISCIPLINA

    def editar_disciplina_salvar(self):
        print("APP DISCIPLINA clicou em editar_disciplina_salvar")

        disciplina = self.st.session_state.editar_disciplina_selecionado

        if self.st.session_state.editar_disciplina_nome:
            disciplina.nome = self.st.session_state.editar_disciplina_nome.upper()
        if self.st.session_state.editar_disciplina_carga_horaria:
            disciplina.carga_horaria = int(
                self.st.session_state.editar_disciplina_carga_horaria)
        if self.st.session_state.editar_disciplina_professor:
            disciplina.nome_professor = self.st.session_state.editar_disciplina_professor.upper()

        erros = disciplina.validar()
        self.st.session_state.erros = erros

        if not erros:
            self.disciplina_db.atualizar(disciplina)
            self.st.session_state.tela = "editar_disciplina_sucesso"

    # EXCLUIR DISCIPLINA

    def excluir_disciplina(self):
        print("APP DISCIPLINA clicou em excluir_disciplina")

        self.st.session_state.excluir_disciplina_erro = None
        self.st.session_state.excluir_disciplina_mensagem = None

        codigo_disciplina = self.st.session_state.excluir_disciplina_codigo_aoconfirmar
        self.st.session_state.excluir_disciplina_codigo_aoconfirmar = None

        nome_disciplina = self.disciplina_db.obter_nome_disciplina_por_codigo(
            codigo_disciplina)
        self.disciplina_db.excluir_por_codigo(codigo_disciplina)
        self.st.session_state.excluir_disciplina_mensagem = f"Disciplina **{nome_disciplina}** excluída com sucesso!"

        self.ir_para_listar_disciplinas()

    # IR PARA TELAS

    def ir_para_listar_disciplinas(self):
        print("APP DISCIPLINA ir_para_listar_disciplinas")

        self.st.session_state.editar_disciplina_codigo = None
        self.st.session_state.excluir_disciplina_codigo = None

        self.st.session_state.tela = "listar_disciplinas"

    def ir_para_nova_disciplina(self):
        print("APP DISCIPLINA ir_para_nova_disciplina")

        self.st.session_state.erros = None

        self.st.session_state.tela = "nova_disciplina"

    def ir_para_editar_disciplina(self):
        print("APP ALUNO ir_para_editar_disciplina")

        self.st.session_state.erros = None
        self.st.session_state.editar_disciplina_erro = None

        codigo_disciplina = self.st.session_state.editar_disciplina_codigo

        eh_codigo_em_uso = self.disciplina_db.verificar_codigo_em_uso(
            codigo_disciplina)
        if not eh_codigo_em_uso:
            self.st.session_state.editar_disciplina_erro = "🪪 Nenhuma Disciplina encontrada com o **CODIGO** informado!"
            return

        disciplina = self.disciplina_db.obter_por_codigo(codigo_disciplina)
        self.st.session_state.editar_disciplina_selecionado = disciplina

        self.st.session_state.tela = "editar_disciplina"

    def ir_para_excluir_disciplina(self):
        print("APP DISCIPLINA ir_para_excluir_disciplina")

        self.st.session_state.excluir_disciplina_erro = None
        self.st.session_state.excluir_disciplina_mensagem = None

        codigo_disciplina = self.st.session_state.excluir_disciplina_codigo
        self.st.session_state.excluir_disciplina_codigo_aoconfirmar = codigo_disciplina

        if not codigo_disciplina or int(codigo_disciplina) <= 0:
            self.st.session_state.excluir_disciplina_erro = "🪪 Informe um CODIGO válido para excluir uma Disciplina!"
            return

        eh_codigo_em_uso = self.disciplina_db.verificar_codigo_em_uso(
            codigo_disciplina)
        if not eh_codigo_em_uso:
            self.st.session_state.excluir_disciplina_erro = "🪪 Nenhuma Disciplina encontrada com o CODIGO informado!"
            return

        self.st.session_state.tela = "excluir_disciplina"

    # EXIBIR TELAS

    def exibir_nova_disciplina_sucesso(self):
        print("APP DISCIPLINA exibir_nova_disciplina_sucesso")

        nova_disciplina = self.obter_nova_disciplina()

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina")
            self.st.button("voltar",
                           help="voltar para a listagem de Disciplinas",
                           on_click=self.ir_para_listar_disciplinas)
            self.st.success("Disciplina salvo com sucesso!", icon="💾")
            self.st.write("🪪", self.st.session_state.nova_disciplina_codigo)
            self.st.write("📘", nova_disciplina.nome, )
            self.st.write("⏳", nova_disciplina.carga_horaria)
            self.st.write("👨‍🏫", nova_disciplina.nome_professor)

    def exibir_nova_disciplina(self):
        print("APP DISCIPLINA exibir_nova_disciplina")

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina | Nova")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            self.st.button("voltar", on_click=self.ir_para_listar_disciplinas,
                           help="**cancelar** o cadastro da nova Disciplina e voltar para a listagem de Disciplinas")
            self.st.write("Informe os dados da nova Disciplina")

            self.st.write(
                "🪪 O **CÓDIGO** da Disciplina será gerado automaticamente")
            self.st.text_input("Nome:",
                               max_chars=200,
                               placeholder="informe o nome da nova Disciplina",
                               icon="📘",
                               key="nova_disciplina_nome")
            self.st.number_input("Carga horária:",
                                 value=1,
                                 min_value=1,
                                 icon="⏳",
                                 key="nova_disciplina_carga_horaria")
            self.st.text_input("Professor:",
                               max_chars=200,
                               placeholder="informe o nome completo do Professor",
                               icon="👨‍🏫",
                               key="nova_disciplina_professor")

            self.st.button("salvar", icon="💾",
                           on_click=self.nova_disciplina_salvar)

            if self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

    def exibir_editar_disciplina_sucesso(self):
        print("APP DISCIPLINA exibir_editar_disciplina_sucesso")

        disciplina = self.st.session_state.editar_disciplina_selecionado

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina")
            self.st.button("voltar",
                           help="voltar para a listagem de Disciplinas",
                           on_click=self.ir_para_listar_disciplinas)
            self.st.success("Disciplina editado com sucesso!", icon="💾")
            self.st.subheader(f"🪪 {disciplina.codigo}")
            self.st.write("📘", disciplina.nome, )
            self.st.write("⏳", disciplina.carga_horaria)
            self.st.write("👨‍🏫", disciplina.nome_professor)

    def exibir_editar_disciplina(self):
        print("APP DISCIPLINA exibir_editar_disciplina")

        disciplina = self.st.session_state.editar_disciplina_selecionado

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina | Editar")
            self.st.button("voltar",
                           help="**cancelar** a edição da Disciplina e voltar para a listagem de Disciplinas",
                           on_click=self.ir_para_listar_disciplinas)
            self.st.subheader(f"🪪 {disciplina.codigo} {disciplina.nome}")
            self.st.write(
                "Preencha somente as informações que deseja alterar e clique em **salvar**")

            self.st.text_input("Nome:", max_chars=200,
                               placeholder="informe o nome completo da nova Disciplina",
                               icon="📘",
                               key="editar_disciplina_nome")
            self.st.number_input("Carga horária:",
                                 value=None,
                                 min_value=1,
                                 icon="⏳",
                                 key="editar_disciplina_carga_horaria")
            self.st.text_input("Professor:",
                               max_chars=200,
                               icon="👨‍🏫",
                               key="editar_disciplina_professor")

            self.st.button("salvar",
                           icon="💾",
                           on_click=self.editar_disciplina_salvar)

            if self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

    def exibir_listar_disciplinas(self):
        print("APP DISCIPLINA exibir_listar_disciplinas")

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina | Lista")

            col1, col2, col3 = self.st.columns([1, 1, 2])
            with col1:
                self.st.button(
                    "nova disciplina", on_click=self.ir_para_nova_disciplina, icon="➕")

            if self.st.session_state.excluir_disciplina_mensagem:
                self.st.success(
                    self.st.session_state.excluir_disciplina_mensagem, icon="🔥")
                self.st.session_state.excluir_disciplina_mensagem = None

            disciplinas = self.disciplina_db.listar()
            if len(disciplinas) == 0:
                self.st.write("nao ha Disciplinas cadastradas")
            else:
                with col2:
                    clicou_em_editar_disciplina = self.st.button("editar disciplina",
                                                                 icon="📝",
                                                                 help="inicia o processo de 📝 **EDITAR** uma Disciplina",)

                with col3:
                    clicou_em_excluir_disciplina = self.st.button("excluir disciplina",
                                                                  icon="🔥",
                                                                  help="inicia o processo de 🔥 **EXCLUIR** uma Disciplina",)
                if clicou_em_editar_disciplina:
                    self.st.chat_input(
                        "📝 para EDITAR uma Disciplina, informe o CODIGO e pressione ENTER",
                        max_chars=10,
                        on_submit=self.ir_para_editar_disciplina,
                        key="editar_disciplina_codigo",)

                if clicou_em_excluir_disciplina:
                    self.st.chat_input(
                        "🔥 para EXCLUIR uma Disciplina, informe o CODIGO e pressione ENTER",
                        max_chars=10,
                        on_submit=self.ir_para_excluir_disciplina,
                        key="excluir_disciplina_codigo")

                if self.st.session_state.editar_disciplina_erro:
                    self.st.error(
                        self.st.session_state.editar_disciplina_erro)
                    self.st.session_state.editar_disciplina_erro = None

                if self.st.session_state.excluir_disciplina_erro:
                    self.st.error(
                        self.st.session_state.excluir_disciplina_erro)
                    self.st.session_state.excluir_disciplina_erro = None

                self.st.write(len(disciplinas),
                              "disciplinas" if len(
                                  disciplinas) > 1 else "disciplina",
                              "cadastradas" if len(disciplinas) > 1 else "cadastrada")

                self.st.dataframe(disciplinas)

    def exibir_excluir_disciplina(self):
        print("APP DISCIPLINA exibir_excluir_disciplina")

        codigo = self.st.session_state.excluir_disciplina_codigo
        disciplina = self.disciplina_db.obter_por_codigo(codigo)

        with self.placeholder.container():
            self.st.subheader("📚 Disciplina | Excluir")
            self.st.button("voltar",
                           help="**cancelar** a exclusão da Disciplina e voltar para a listagem de Disciplinas",
                           on_click=self.ir_para_listar_disciplinas)
            self.st.write(
                f"Você está prestes a excluir a Disciplina **{disciplina.nome}**")

            self.st.write("🪪", disciplina.codigo)
            self.st.write("⏳", disciplina.carga_horaria)
            self.st.write("👨‍🏫", disciplina.nome_professor)

            self.st.button("confirmar exclusão", icon="🔥",
                           on_click=self.excluir_disciplina)

    # EXIBIR PRINCIPAL

    def exibir(self):
        if self.st.session_state.tela == "nova_disciplina_sucesso":
            self.exibir_nova_disciplina_sucesso()
        elif self.st.session_state.tela == "nova_disciplina":
            self.exibir_nova_disciplina()
        elif self.st.session_state.tela == "editar_disciplina_sucesso":
            self.exibir_editar_disciplina_sucesso()
        elif self.st.session_state.tela == "editar_disciplina":
            self.exibir_editar_disciplina()
        elif self.st.session_state.tela == "excluir_disciplina":
            self.exibir_excluir_disciplina()
        else:  # listar_disciplinas
            self.exibir_listar_disciplinas()
