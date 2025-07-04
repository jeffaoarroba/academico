from datetime import datetime
from banco.aluno_db import AlunoDB
from tipo.aluno import Aluno
from servico.via_cep import ViaCEP
from util import gerar_endereco_completo


class AlunoApp:

    def __init__(self, st, placeholder, aluno_db: AlunoDB):
        self.st = st
        self.placeholder = placeholder
        self.aluno_db = aluno_db

    # NOVO ALUNO

    def obter_novo_aluno(self):
        if self.st.session_state.novo_aluno_cep_erro:
            self.st.session_state.novo_aluno_endereco = gerar_endereco_completo(
                self.st.session_state.novo_aluno_logradouro,
                self.st.session_state.novo_aluno_bairro,
                self.st.session_state.novo_aluno_cidade,
                self.st.session_state.novo_aluno_estado,
                self.st.session_state.novo_aluno_cep
            )
        return Aluno(
            self.st.session_state.novo_aluno_cpf,
            self.st.session_state.novo_aluno_nome,
            self.st.session_state.novo_aluno_ano,
            self.st.session_state.novo_aluno_email,
            self.st.session_state.novo_aluno_endereco
        )

    def novo_aluno_salvar(self):
        print("APP ALUNO clicou em salvar novo aluno")
        novo_aluno = self.obter_novo_aluno()
        erros = novo_aluno.validar()
        cpf_ja_existe = self.aluno_db.verificar_cpf_em_uso(novo_aluno.cpf)
        if cpf_ja_existe:
            erros.insert(0, "🪪 O **CPF** informado já está sendo utilizado")
        if not erros:
            self.aluno_db.cadastrar(novo_aluno)
            self.st.session_state.tela = "novo_aluno_sucesso"
        self.st.session_state.erros = erros

    # EDITAR ALUNO

    def editar_aluno_salvar(self):
        print("APP ALUNO clicou em salvar editar aluno")
        aluno = self.st.session_state.editar_aluno_selecionado
        if self.st.session_state.editar_aluno_nome:
            aluno.nome = self.st.session_state.editar_aluno_nome.upper()
        if self.st.session_state.editar_aluno_ano:
            aluno.ano_nascimento = int(
                self.st.session_state.editar_aluno_ano)
        if self.st.session_state.editar_aluno_email:
            aluno.email = self.st.session_state.editar_aluno_email.upper()
        if self.st.session_state.editar_aluno_cep and not self.st.session_state.editar_aluno_cep_erro and self.st.session_state.editar_aluno_endereco:
            aluno.endereco = self.st.session_state.editar_aluno_endereco
        if self.st.session_state.editar_aluno_cep_erro and not self.st.session_state.editar_aluno_endereco and (
                self.st.session_state.editar_aluno_logradouro or
                self.st.session_state.editar_aluno_bairro or
                self.st.session_state.editar_aluno_cidade or
                self.st.session_state.editar_aluno_estado or
                self.st.session_state.editar_aluno_cep
        ):
            aluno.endereco = gerar_endereco_completo(
                self.st.session_state.editar_aluno_logradouro,
                self.st.session_state.editar_aluno_bairro,
                self.st.session_state.editar_aluno_cidade,
                self.st.session_state.editar_aluno_estado,
                self.st.session_state.editar_aluno_cep
            )
        erros = aluno.validar()
        self.st.session_state.erros = erros
        if not erros:
            self.aluno_db.atualizar(aluno)
            self.st.session_state.tela = "editar_aluno_sucesso"

    def editar_aluno_cpf(self):
        print("TESTE")

    # EXCLUIR ALUNO

    def excluir_aluno(self):
        print("APP ALUNO clicou em excluir aluno")
        cpf = self.st.session_state.excluir_aluno_cpf_aoconfirmar
        if not cpf:
            self.st.session_state.excluir_aluno_cpf_erro = "🪪 Informe um CPF válido para excluir um Aluno!"
            return

        eh_cpf_valido = Aluno.validar_cpf(None, cpf)
        if not eh_cpf_valido:
            self.st.session_state.excluir_aluno_cpf_erro = "🪪 Informe um CPF válido para excluir um Aluno!"
            return

        eh_cpf_em_uso = self.aluno_db.verificar_cpf_em_uso(cpf)
        if not eh_cpf_em_uso:
            self.st.session_state.excluir_aluno_cpf_erro = "🪪 Nenhum Aluno encontrado com o CPF informado."
            return

        nome_aluno = self.aluno_db.obter_nome_aluno_por_cpf(int(cpf))
        self.aluno_db.excluir_por_cpf(int(cpf))
        self.st.session_state.excluir_aluno_mensagem = f"🔥 Aluno **{nome_aluno}** excluído com sucesso!"
        self.st.session_state.tela = "listar_alunos"

    # IR PARA TELAS

    def ir_para_listar_alunos(self):
        self.st.session_state.editar_aluno_cpf_erro = None
        self.st.session_state.excluir_aluno_cpf_erro = None
        self.st.session_state.excluir_aluno_cpf_aoconfirmar = None
        self.st.session_state.tela = "listar_alunos"

    def ir_para_novo_aluno(self):
        self.st.session_state.novo_aluno_cep_erro = False
        self.st.session_state.novo_aluno_endereco = ""
        self.st.session_state.tela = "novo_aluno"

    def ir_para_editar_aluno(self):
        self.st.session_state.editar_aluno_cep_erro = False
        self.st.session_state.editar_aluno_endereco = ""

        cpf = self.st.session_state.editar_aluno_cpf
        eh_cpf_valido = Aluno.validar_cpf(None, cpf)
        if not eh_cpf_valido:
            self.st.session_state.editar_aluno_cpf_erro = "🪪 Informe um CPF válido para editar um Aluno!"
            return

        eh_cpf_em_uso = self.aluno_db.verificar_cpf_em_uso(cpf)
        if not eh_cpf_em_uso:
            self.st.session_state.editar_aluno_cpf_erro = "🪪 Nenhum Aluno encontrado com o CPF informado."
            return

        self.st.session_state.editar_aluno_selecionado = self.aluno_db.obter_por_cpf(
            int(cpf))
        self.st.session_state.tela = "editar_aluno"

    def ir_para_excluir_aluno(self):
        self.st.session_state.excluir_aluno_cpf_confirmado = None
        self.st.session_state.excluir_aluno_cpf_erro = None
        cpf = self.st.session_state.excluir_aluno_cpf

        eh_cpf_valido = Aluno.validar_cpf(None, cpf)
        if not eh_cpf_valido:
            self.st.session_state.excluir_aluno_cpf_erro = "🪪 Informe um CPF válido para excluir um Aluno!"
            return

        eh_cpf_em_uso = self.aluno_db.verificar_cpf_em_uso(cpf)
        if not eh_cpf_em_uso:
            self.st.session_state.excluir_aluno_cpf_erro = "🪪 Nenhum Aluno encontrado com o CPF informado."
            return

        self.st.session_state.tela = "excluir_aluno"

    # EXIBIR TELAS

    def exibir_novo_aluno_sucesso(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno")
            self.st.button("voltar",
                           help="voltar para a listagem de Alunos",
                           on_click=self.ir_para_listar_alunos)
            self.st.success("Aluno salvo com sucesso!")
            novo_aluno = self.obter_novo_aluno()
            self.st.write("🧑", novo_aluno.nome, )
            self.st.write("🪪", novo_aluno.cpf)
            self.st.write("🗓️", novo_aluno.ano_nascimento)
            self.st.write("✉️", novo_aluno.email)
            self.st.write("🛣️", novo_aluno.endereco)

    def exibir_novo_aluno(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Novo")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            self.st.button("voltar", on_click=self.ir_para_listar_alunos,
                           help="**cancelar** o cadastro do novo aluno e voltar para a listagem de alunos")
            self.st.write("Informe os dados do novo Aluno")

            self.st.text_input("CPF:",
                               max_chars=11,
                               placeholder="informe somente os numeros do CPF",
                               icon="🪪",
                               key="novo_aluno_cpf")
            self.st.text_input("Nome:",
                               max_chars=200,
                               placeholder="informe o nome completo do novo aluno",
                               icon="🧑",
                               key="novo_aluno_nome")
            self.st.number_input("Ano de Nascimento:",
                                 value=None,
                                 min_value=1970,
                                 max_value=datetime.now().year - 1,
                                 help="se a data de nascimento do Aluno é 01/02/2003, informe somente o ano 2003",
                                 placeholder="informe somente o ANO da data de nascimento do Aluno",
                                 icon="🗓️",
                                 key="novo_aluno_ano")
            self.st.text_input("Email:",
                               max_chars=200,
                               icon="✉️",
                               key="novo_aluno_email")

            self.st.text_input("CEP:",
                               max_chars=200,
                               placeholder="informe somente os numeros do CEP",
                               icon="🛣️",
                               key="novo_aluno_cep")

            clicou_em_consultar_cep = self.st.button("consultar CEP", icon="🔎")

            if clicou_em_consultar_cep:
                self.st.session_state.novo_aluno_cep_erro = False
                self.st.session_state.novo_aluno_endereco = ""
                try:
                    if self.st.session_state.novo_aluno_cep:
                        print("APP ALUNOS NOVO_ALUNO consultar_cep",
                              self.st.session_state.novo_aluno_cep)
                        consulta_cep = ViaCEP(
                            self.st.session_state.novo_aluno_cep).obter_endereco_completo()
                        if consulta_cep['erro']:
                            print("ERRO APP ALUNOS NOVO_ALUNO consultar_cep",
                                  consulta_cep['erro'])
                            self.st.session_state.novo_aluno_cep_erro = consulta_cep['erro']
                        else:
                            print("APP ALUNOS NOVO_ALUNO endereco_completo",
                                  consulta_cep['endereco_completo'])
                            self.st.session_state.novo_aluno_endereco = consulta_cep[
                                'endereco_completo']
                            # self.st.write(consulta_cep['endereco_completo'])
                    else:
                        print("APP ALUNOS NOVO_ALUNO cep não informado")
                        self.st.session_state.novo_aluno_cep_erro = "🛣️ CEP não informado"
                except Exception as e:
                    print("ERRO APP ALUNOS NOVO_ALUNO consultar_cep", e)
                    self.st.session_state.novo_aluno_cep_erro = e

                if not self.st.session_state.novo_aluno_cep_erro:
                    self.st.text_input("Endereço",
                                       disabled=True,
                                       value=self.st.session_state.novo_aluno_endereco)

            if self.st.session_state.novo_aluno_cep_erro:
                self.st.error(self.st.session_state.novo_aluno_cep_erro)

                self.st.text_input("Logradouro:",
                                   max_chars=200,
                                   placeholder="nome da rua e numero da casa",
                                   key="novo_aluno_logradouro")
                self.st.text_input("Bairro:",
                                   max_chars=200,
                                   key="novo_aluno_bairro")
                self.st.text_input("Cidade:",
                                   max_chars=200,
                                   key="novo_aluno_cidade")
                self.st.text_input("Estado:",
                                   max_chars=2,
                                   help="Informe a sigla do Estado (UF) para 'Espirito Santo' informe somente **ES**",
                                   placeholder="informa a sigla do estado (UF)",
                                   key="novo_aluno_estado")

            self.st.button("salvar", icon="💾", on_click=self.novo_aluno_salvar)

            if "erros" in self.st.session_state and self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

    def exibir_editar_aluno_sucesso(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno")
            self.st.button("voltar",
                           help="voltar para a listagem de Alunos",
                           on_click=self.ir_para_listar_alunos)
            self.st.success("Aluno editado com sucesso!")
            aluno = self.st.session_state.editar_aluno_selecionado
            self.st.subheader(f"🪪 {aluno.cpf}")
            self.st.write("🧑", aluno.nome, )
            self.st.write("🗓️", aluno.ano_nascimento)
            self.st.write("✉️", aluno.email)
            self.st.write("🛣️", aluno.endereco)

    def exibir_editar_aluno(self):
        aluno = self.st.session_state.editar_aluno_selecionado

        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Editar")
            self.st.button("voltar",
                           help="**cancelar** a edição do Aluno e voltar para a listagem de alunos",
                           on_click=self.ir_para_listar_alunos)
            self.st.subheader(f"🪪 {aluno.cpf} {aluno.nome}")
            self.st.write(
                "Preencha somente as informações que deseja alterar e clique em **salvar**")
            self.st.text_input("Nome:", max_chars=200,
                               placeholder="informe o nome completo do novo aluno",
                               icon="🧑",
                               key="editar_aluno_nome")
            self.st.number_input("Ano de Nascimento:",
                                 value=None,
                                 min_value=1970,
                                 max_value=datetime.now().year - 1,
                                 help="se a data de nascimento do Aluno é 01/02/2003, informe somente o ano 2003",
                                 placeholder="informe somente o ANO da data de nascimento do Aluno",
                                 icon="🗓️",
                                 key="editar_aluno_ano")
            self.st.text_input("Email:",
                               max_chars=200,
                               icon="✉️",
                               key="editar_aluno_email")
            self.st.text_input("CEP:",
                               max_chars=200,
                               placeholder="informe somente os numeros do CEP",
                               icon="🛣️",
                               key="editar_aluno_cep")

            clicou_em_consultar_cep = self.st.button("consultar CEP", icon="🔎")

            if clicou_em_consultar_cep:
                self.st.session_state.editar_aluno_cep_erro = False
                self.st.session_state.editar_aluno_endereco = ""
                try:
                    if self.st.session_state.editar_aluno_cep:
                        print("APP ALUNOS EDITAR_ALUNO consultar_cep",
                              self.st.session_state.editar_aluno_cep)
                        consulta_cep = ViaCEP(
                            self.st.session_state.editar_aluno_cep).obter_endereco_completo()
                        if consulta_cep['erro']:
                            print("ERRO APP ALUNOS EDITAR_ALUNO consultar_cep",
                                  consulta_cep['erro'])
                            self.st.session_state.editar_aluno_cep_erro = consulta_cep['erro']
                        else:
                            print("APP ALUNOS EDITAR_ALUNO endereco_completo",
                                  consulta_cep['endereco_completo'])
                            self.st.session_state.editar_aluno_endereco = consulta_cep[
                                'endereco_completo']
                            # self.st.write(consulta_cep['endereco_completo'])
                    else:
                        print("APP ALUNOS EDITAR_ALUNO cep não informado")
                        self.st.session_state.editar_aluno_cep_erro = "🛣️ CEP não informado"
                except Exception as e:
                    print("ERRO APP ALUNOS EDITAR_ALUNO consultar_cep", e)
                    self.st.session_state.editar_aluno_cep_erro = e

                if not self.st.session_state.editar_aluno_cep_erro:
                    self.st.text_input("Endereço",
                                       disabled=True,
                                       value=self.st.session_state.editar_aluno_endereco)

            if self.st.session_state.editar_aluno_cep_erro:
                self.st.error(self.st.session_state.editar_aluno_cep_erro)
                self.st.write(
                    """
                    Para não atualizar o **Endereço do Aluno**, deixe todos os campos abaixo em branco
                    """)

                self.st.text_input("Logradouro:",
                                   max_chars=200,
                                   placeholder="nome da rua e numero da casa",
                                   key="editar_aluno_logradouro")
                self.st.text_input("Bairro:",
                                   max_chars=200,
                                   key="editar_aluno_bairro")
                self.st.text_input("Cidade:",
                                   max_chars=200,
                                   key="editar_aluno_cidade")
                self.st.text_input("Estado:",
                                   max_chars=2,
                                   help="Informe a sigla do Estado (UF) para 'Espirito Santo' informe somente **ES**",
                                   placeholder="informa a sigla do estado (UF)",
                                   key="editar_aluno_estado")

            self.st.button("salvar",
                           icon="💾",
                           on_click=self.editar_aluno_salvar)

            if "erros" in self.st.session_state and self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

    def exibir_listar_alunos(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Lista")
            col1, col2, col3 = self.st.columns([1, 1, 2])
            with col1:
                self.st.button(
                    "novo aluno", on_click=self.ir_para_novo_aluno, icon="➕")

            if "excluir_aluno_mensagem" in self.st.session_state and self.st.session_state.excluir_aluno_mensagem:
                self.st.success(
                    self.st.session_state.excluir_aluno_mensagem)
                self.st.session_state.excluir_aluno_mensagem = None

            alunos = self.aluno_db.listar()
            if len(alunos) == 0:
                self.st.write("nao ha alunos cadastrados")
            else:
                with col2:
                    clicou_em_editar_aluno = self.st.button("editar aluno",
                                                            icon="📝",
                                                            help="inicia o processo de 📝 **EDITAR** um Aluno",)

                with col3:
                    clicou_em_excluir_aluno = self.st.button("excluir aluno",
                                                             icon="🔥",
                                                             help="inicia o processo de 🔥 **EXCLUIR** um Aluno",)
                if clicou_em_editar_aluno:
                    self.st.chat_input(
                        "📝 para EDITAR um aluno, informe o CPF e pressione ENTER",
                        max_chars=11,
                        on_submit=self.ir_para_editar_aluno,
                        key="editar_aluno_cpf",)
                if clicou_em_excluir_aluno:
                    self.st.chat_input(
                        "🔥 para EXCLUIR um aluno, informe o CPF e pressione ENTER",
                        max_chars=11,
                        on_submit=self.ir_para_excluir_aluno,
                        key="excluir_aluno_cpf")

                if "editar_aluno_cpf_erro" in self.st.session_state and self.st.session_state.editar_aluno_cpf_erro:
                    self.st.error(
                        self.st.session_state.editar_aluno_cpf_erro)
                    self.st.session_state.editar_aluno_cpf_erro = None

                if "excluir_aluno_cpf_erro" in self.st.session_state and self.st.session_state.excluir_aluno_cpf_erro:
                    self.st.error(
                        self.st.session_state.excluir_aluno_cpf_erro)
                    self.st.session_state.excluir_aluno_cpf_erro = None

                self.st.dataframe(alunos)

    def exibir_excluir_aluno(self):
        cpf = self.st.session_state.excluir_aluno_cpf
        self.st.session_state.excluir_aluno_cpf_aoconfirmar = cpf
        aluno = self.aluno_db.obter_por_cpf(int(cpf))

        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Excluir")
            self.st.button("voltar",
                           help="**cancelar** a exclusão do Aluno e voltar para a listagem de alunos",
                           on_click=self.ir_para_listar_alunos)
            if aluno:
                self.st.write(
                    f"Você está prestes a excluir o Aluno **{aluno.nome}**")
                self.st.write("🪪", aluno.cpf)
                self.st.write("🗓️", aluno.ano_nascimento)
                self.st.write("✉️", aluno.email)
                self.st.write("🛣️", aluno.endereco)
                self.st.button("confirmar exclusão", icon="🔥",
                               on_click=self.excluir_aluno)

    # EXIBIR PRINCIPAL

    def exibir(self):
        if self.st.session_state.tela == "novo_aluno_sucesso":
            self.exibir_novo_aluno_sucesso()
        elif self.st.session_state.tela == "novo_aluno":
            self.exibir_novo_aluno()
        elif self.st.session_state.tela == "editar_aluno_sucesso":
            self.exibir_editar_aluno_sucesso()
        elif self.st.session_state.tela == "editar_aluno":
            self.exibir_editar_aluno()
        elif self.st.session_state.tela == "excluir_aluno":
            self.exibir_excluir_aluno()
        else:  # listar_alunos
            self.exibir_listar_alunos()

        # debug de variaveis de sessao
        # self.st.write(self.st.session_state)
