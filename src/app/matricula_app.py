from datetime import datetime
from banco.matricula_db import MatriculaDB
from banco.disciplina_db import DisciplinaDB
from banco.aluno_db import AlunoDB
from tipo.matricula import Matricula
from util import eh_cpf_valido


class MatriculaApp:

    def __init__(self, st, placeholder, matricula_db: MatriculaDB, aluno_db: AlunoDB, disciplina_db: DisciplinaDB):
        self.st = st
        self.placeholder = placeholder
        self.matricula_db = matricula_db
        self.aluno_db = aluno_db
        self.disciplina_db = disciplina_db
        if "cancelar_matricula_erro" in self.st.session_state:
            self.st.session_state.cancelar_matricula_erro = None
        if not "exibir_cancelar_matricula" in self.st.session_state:
            self.st.session_state.exibir_cancelar_matricula = False
        # debug de variaveis de sessao
        # self.st.write(self.st.session_state)

    # NOVA MATRICULA

    def obter_nova_matricula(self):
        return Matricula(
            self.st.session_state.nova_matricula_disciplina.codigo,
            self.st.session_state.nova_matricula_aluno.cpf,
        )

    def nova_matricula_verificar_dados(self):
        print("APP MATRICULA clicou em nova_matricula_verificar_dados")

        self.st.session_state.nova_matricula_disciplina = None
        self.st.session_state.nova_matricula_aluno = None

        codigo_disciplina = self.st.session_state.nova_matricula_codigo_disciplina
        cpf_aluno = self.st.session_state.nova_matricula_cpf_aluno

        self.st.session_state.erros = []

        # DISCIPLINA
        if not codigo_disciplina:
            self.st.session_state.erros.append(
                "📘 Informe o **CODIGO** da Disciplina")
        elif not self.disciplina_db.verificar_codigo_em_uso(codigo_disciplina):
            self.st.session_state.erros.append(
                "📘 O **CODIGO** da Disciplina informado não está cadastrado")
        else:
            # se o CODIGO da Disciplina for valido e estiver cadastrado
            # entao obtem a Disciplina para preencher na matricula
            self.st.session_state.nova_matricula_disciplina = self.disciplina_db.obter_por_codigo(
                codigo_disciplina)

        # ALUNO
        if not cpf_aluno:
            self.st.session_state.erros.append(
                "🧑‍🎓 Informe o **CPF** do Aluno")
        else:
            if not eh_cpf_valido(cpf_aluno):
                self.st.session_state.erros.append(
                    "🧑‍🎓 Informe um **CPF** válido do Aluno")
            elif not self.aluno_db.verificar_cpf_em_uso(cpf_aluno):
                self.st.session_state.erros.append(
                    "🧑‍🎓 O **CPF** do Aluno informado não está cadastrado")
            else:
                # se o CPF do Aluno for valido e estiver cadastrado
                # entao obtem o nome do Aluno para preencher na matricula
                self.st.session_state.nova_matricula_aluno = self.aluno_db.obter_por_cpf(
                    cpf_aluno)

    def nova_matricula_salvar(self):
        print("APP MATRICULA clicou em nova_matricula_salvar")
        nova_matricula = self.obter_nova_matricula()
        erros = nova_matricula.validar()
        if not erros:
            self.matricula_db.cadastrar(nova_matricula)
            self.st.session_state.tela = "nova_matricula_sucesso"
        self.st.session_state.erros = erros

    # CANCELAR MATRICULA

    def alternar_cancelar_matricula(self):
        self.st.session_state.exibir_cancelar_matricula = not self.st.session_state.exibir_cancelar_matricula

    def clicou_em_cancelar_matricula_voltar(self):
        self.alternar_cancelar_matricula()
        self.ir_para_listar_matriculas()

    def clicou_em_cancelar_matricula_continuar(self):
        self.st.session_state.cancelar_matricula_erro = None
        codigo_disciplina = self.st.session_state.cancelar_matricula_codigo_disciplina
        cpf_aluno = self.st.session_state.cancelar_matricula_cpf_aluno

        if not codigo_disciplina:
            self.st.session_state.cancelar_matricula_erro = "🪪❓ Informe o **CODIGO** da Disciplina para cancelar uma Matricula."
            return
        if not cpf_aluno:
            self.st.session_state.cancelar_matricula_erro = "🪪❓ Informe o **CPF** do Aluno para cancelar uma Matricula."
            return
        if not int(codigo_disciplina) > 0:
            self.st.session_state.cancelar_matricula_erro = "🪪❓ Informe um **CODIGO** válido da Disciplina para cancelar uma Matricula."
            return
        if not eh_cpf_valido(cpf_aluno):
            self.st.session_state.cancelar_matricula_erro = "🪪❓ Informe um **CPF** válido do Aluno para cancelar uma Matricula."
            return
        estah_em_uso = self.matricula_db.verificar_em_uso(
            codigo_disciplina, cpf_aluno)
        if not estah_em_uso:
            self.st.session_state.cancelar_matricula_erro = "🪪❓ Nenhuma Matricula encontrada."
            return

        self.st.session_state.tela = "cancelar_matricula"

    def cancelar_matricula(self):
        print("APP MATRICULA clicou em continuar_cancelar_matricula")

        codigo_disciplina = self.st.session_state.cancelar_matricula_codigo_disciplina_aoconfirmar
        cpf_aluno = self.st.session_state.cancelar_matricula_cpf_aluno_aoconfirmar

        self.st.session_state.cancelar_matricula_codigo_disciplina_aoconfirmar = None
        self.st.session_state.cancelar_matricula_cpf_aluno_aoconfirmar = None

        self.matricula_db.excluir_por(codigo_disciplina, cpf_aluno)
        self.st.session_state.cancelar_matricula_mensagem = f"🔥 Matricula excluída com sucesso!"
        self.alternar_cancelar_matricula()
        self.st.session_state.tela = "listar_matriculas"

    # IR PARA TELAS

    def ir_para_listar_matriculas(self):
        self.st.session_state.tela = "listar_matriculas"

    def ir_para_nova_matricula(self):
        self.st.session_state.nova_matricula_aluno = None
        self.st.session_state.nova_matricula_disciplina = None
        self.st.session_state.tela = "nova_matricula"

    # EXIBIR TELAS

    def exibir_nova_matricula_sucesso(self):
        with self.placeholder.container():
            self.st.subheader("📝🎓 Matricula")
            self.st.button("voltar",
                           help="voltar para a listagem de matriculas",
                           on_click=self.ir_para_listar_matriculas)
            self.st.success("Matricula salvo com sucesso!", icon="💾")
            nova_matricula = self.matricula_db.obter_por(
                self.st.session_state.nova_matricula_codigo_disciplina,
                self.st.session_state.nova_matricula_cpf_aluno)
            self.st.write("**MATRICULA**")
            self.st.write("📘", nova_matricula.nome_disciplina, )
            self.st.write("👨‍🏫", nova_matricula.nome_professor_disciplina)
            self.st.write("**ALUNO**")
            self.st.write("🧑‍🎓", nova_matricula.nome_aluno,
                          f"`{nova_matricula.cpf_aluno}`")
            self.st.write("✉️", nova_matricula.email_aluno)
            self.st.write("🛣️", nova_matricula.endereco_aluno)

    def exibir_nova_matricula(self):
        with self.placeholder.container():
            self.st.subheader("📝🎓 Matricula | Nova")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            self.st.button("voltar", on_click=self.ir_para_listar_matriculas,
                           help="**cancelar** o cadastro da nova matricula e voltar para a listagem de matriculas")
            self.st.write("Informe os dados da nova matricula")

            col1, col2 = self.st.columns(2)
            with col1:
                self.st.text_input("Disciplina:",
                                   max_chars=10,
                                   placeholder="CODIGO da Disciplina",
                                   icon="📘",
                                   key="nova_matricula_codigo_disciplina")
            with col2:
                self.st.text_input("Aluno:",
                                   max_chars=11,
                                   placeholder="CPF do Aluno",
                                   icon="🧑‍🎓",
                                   key="nova_matricula_cpf_aluno")

            self.st.button("verificar dados", icon="🔍",
                           on_click=self.nova_matricula_verificar_dados)

            if "erros" in self.st.session_state and self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

            disciplina = None
            aluno = None

            if "nova_matricula_disciplina" in self.st.session_state and self.st.session_state.nova_matricula_disciplina:
                disciplina = self.st.session_state.nova_matricula_disciplina
                self.st.subheader(f"📘 {disciplina.nome}")
                #
                # debug
                # self.st.write(disciplina)
                #
                self.st.write(f"⏳ `{disciplina.carga_horaria}` horas")
                self.st.write("👨‍🏫", disciplina.nome_professor)

            if "nova_matricula_aluno" in self.st.session_state and self.st.session_state.nova_matricula_aluno:
                aluno = self.st.session_state.nova_matricula_aluno
                self.st.subheader(f"🧑‍🎓 {aluno.nome}")
                #
                # debug
                # self.st.write(aluno)
                #
                self.st.write(
                    f"🗓️ {aluno.ano_nascimento} (`{aluno.idade} anos`)")
                self.st.write("✉️", aluno.email)
                self.st.write("🛣️", aluno.endereco)

            matricula_em_uso = False
            if disciplina and aluno:
                matricula_em_uso = self.matricula_db.verificar_em_uso(
                    disciplina.codigo,
                    aluno.cpf

                )

            if not matricula_em_uso:
                self.st.button("salvar nova matricula", icon="💾",
                               disabled=matricula_em_uso,
                               on_click=self.nova_matricula_salvar)
            else:
                self.st.warning(
                    "⚠️ O Aluno jah estah Matriculado nessa Disciplina")

    def exibir_listar_matriculas(self):
        with self.placeholder.container():
            self.st.subheader("📝🎓 Matricula | Lista")
            col1, col2 = self.st.columns([1, 3])
            with col1:
                self.st.button(
                    "nova matricula", on_click=self.ir_para_nova_matricula, icon="➕")

            if "cancelar_matricula_mensagem" in self.st.session_state and self.st.session_state.cancelar_matricula_mensagem:
                self.st.success(
                    self.st.session_state.cancelar_matricula_mensagem)
                self.st.session_state.cancelar_matricula_mensagem = None

            matriculas = self.matricula_db.listar()
            if len(matriculas) == 0:
                self.st.write("nao ha matriculas cadastradas")
            else:
                with col2:
                    self.st.button("cancelar matricula",
                                   icon="🔥",
                                   help="inicia o processo de 🔥 **CANCELAR** uma Matricula",
                                   on_click=self.alternar_cancelar_matricula)

                if self.st.session_state.exibir_cancelar_matricula:
                    self.st.write(
                        "Informe o **CODIGO** da Disciplina e o **CPF** do Aluno para cancelar uma Matricula")
                    cancelar_matricula_col1, cancelar_matricula_col2 = self.st.columns([
                                                                                       1, 1])
                    with cancelar_matricula_col1:
                        self.st.text_input(
                            "CODIGO da Disciplina",
                            max_chars=10,
                            key="cancelar_matricula_codigo_disciplina")
                    with cancelar_matricula_col2:
                        self.st.text_input(
                            "CPF do Aluno",
                            max_chars=11,
                            key="cancelar_matricula_cpf_aluno")
                    self.st.button(
                        "continuar",
                        help="validar os dados informados e exibir a **MATRICULA** encontrada",
                        icon="🔥",
                        on_click=self.clicou_em_cancelar_matricula_continuar)

                if "cancelar_matricula_erro" in self.st.session_state and self.st.session_state.cancelar_matricula_erro:
                    self.st.error(
                        self.st.session_state.cancelar_matricula_erro)
                    self.st.session_state.cancelar_matricula_erro = None

                self.st.write(len(matriculas),
                              "matriculas" if len(
                                  matriculas) > 1 else "matricula",
                              "cadastradas" if len(matriculas) > 1 else "cadastrada")

                self.st.dataframe(matriculas)

    def exibir_cancelar_matricula(self):
        codigo_disciplina = self.st.session_state.cancelar_matricula_codigo_disciplina
        cpf_aluno = self.st.session_state.cancelar_matricula_cpf_aluno

        self.st.session_state.cancelar_matricula_codigo_disciplina_aoconfirmar = codigo_disciplina
        self.st.session_state.cancelar_matricula_cpf_aluno_aoconfirmar = cpf_aluno

        matricula = self.matricula_db.obter_por(codigo_disciplina, cpf_aluno)

        with self.placeholder.container():
            self.st.subheader("📝🎓 Matricula | Cancelar")
            self.st.button("voltar",
                           help="não **cancelar** a Matricula e voltar para a listagem de Matriculas",
                           on_click=self.clicou_em_cancelar_matricula_voltar)
            self.st.write(
                f"Você está prestes a **CANCELAR** a Matricula abaixo")

            self.st.subheader("**DISCIPLINA**")
            self.st.write(
                "📘", f"`{matricula.codigo_disciplina}` {matricula.nome_disciplina}")
            self.st.write("👨‍🏫", matricula.nome_professor_disciplina)

            self.st.subheader("**ALUNO**")
            self.st.write(
                "🧑‍🎓", f"`{matricula.cpf_aluno}` {matricula.nome_aluno}")
            self.st.write("✉️", matricula.email_aluno)

            self.st.button("confirmar cancelamento da Matricula 🔥", icon="🔥",
                           on_click=self.cancelar_matricula)

    # EXIBIR PRINCIPAL

    def exibir(self):
        if self.st.session_state.tela == "nova_matricula_sucesso":
            self.exibir_nova_matricula_sucesso()
        elif self.st.session_state.tela == "nova_matricula":
            self.exibir_nova_matricula()
        elif self.st.session_state.tela == "cancelar_matricula":
            self.exibir_cancelar_matricula()
        else:  # listar_matriculas
            self.exibir_listar_matriculas()
