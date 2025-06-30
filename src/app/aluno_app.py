from datetime import datetime
from tipos.aluno import Aluno


class AlunoApp:

    def __init__(self, st, placeholder, aluno_db):
        self.st = st
        self.placeholder = placeholder
        self.aluno_db = aluno_db

    def obter_novo_aluno(self):
        return Aluno(
            self.st.session_state.novo_aluno_cpf,
            self.st.session_state.novo_aluno_nome,
            self.st.session_state.novo_aluno_ano,
            self.st.session_state.novo_aluno_email,
            self.st.session_state.novo_aluno_endereco
        )

    def salvar(self):
        print("APP ALUNO clicou em salvar novo aluno")
        novo_aluno = self.obter_novo_aluno()
        erros = novo_aluno.validar()
        cpf_ja_existe = self.aluno_db.cpf_ja_existe(novo_aluno.cpf)
        if cpf_ja_existe:
            erros.insert(0, "🪪 O **CPF** informado já está sendo utilizado")
        if not erros:
            self.aluno_db.cadastrar(novo_aluno)
            self.st.session_state.tela = "novo_aluno_sucesso"
        self.st.session_state.erros = erros

    def ir_para_lista_alunos(self):
        self.st.session_state.menu = "Alunos"
        self.st.session_state.tela = "listagem"

    def ir_para_novo_aluno(self):
        self.st.session_state.menu = "Alunos"
        self.st.session_state.tela = "novo_aluno"

    def exibir_novo_aluno_sucesso(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno")
            self.st.button("voltar", on_click=self.ir_para_lista_alunos, help="voltar para a listagem de alunos")
            self.st.success("Aluno salvo com sucesso!")
            novo_aluno = self.obter_novo_aluno()
            self.st.write("🧑", novo_aluno.nome)
            self.st.write("🪪", novo_aluno.cpf)
            self.st.write("🗓️", novo_aluno.ano_nascimento)
            self.st.write("✉️", novo_aluno.email)
            self.st.write("🛣️", novo_aluno.endereco)

    def consultar_cep(self):
        print("cep", self.st.session_state.novo_aluno_cep)

    def exibir_novo_aluno(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Novo")
            # os asteriscos em help=**cancelar** aplica o estilo negrito (markdown)
            self.st.button("voltar", on_click=self.ir_para_lista_alunos,
                           help="**cancelar** o cadastro do novo aluno e voltar para a listagem de alunos")
            #with self.st.form("novo_aluno"):
            self.st.write("Informe os dados do novo Aluno")

            cpf = self.st.text_input("CPF:", max_chars=11, placeholder="informe somente os numeros do CPF",
                                     icon="🪪",
                                     key="novo_aluno_cpf")
            nome = self.st.text_input("Nome:", max_chars=200,
                                      placeholder="informe o nome completo do novo aluno",
                                      icon="🧑", key="novo_aluno_nome")
            ano_nascimento = self.st.number_input("Ano de Nascimento:", value=None, min_value=1970,
                                                  max_value=datetime.now().year - 1,
                                                  help="se a data de nascimento do Aluno é 01/02/2003, informe somente o ano 2003",
                                                  placeholder="informe somente o ANO da data de nascimento do Aluno",
                                                  icon="🗓️", key="novo_aluno_ano")
            email = self.st.text_input("Email:", max_chars=200, icon="✉️", key="novo_aluno_email")

            cep = self.st.text_input("CEP:", placeholder="informe somente os numeros do CEP", max_chars=200,
                                     icon="🛣️", key="novo_aluno_cep")

            self.st.button("consultar CEP", icon="💾", on_click=self.consultar_cep)

            logradouro = self.st.text_input("Logradouro:", placeholder="rua Canela, 110", max_chars=200,
                                            key="novo_aluno_logradouro")
            bairro = self.st.text_input("Bairro:", placeholder="Centro", max_chars=200,
                                        key="novo_aluno_bairro")
            cidade = self.st.text_input("Cidade:", placeholder="Serra", max_chars=200,
                                        key="novo_aluno_cidade")
            estado = self.st.text_input("Estado:", placeholder="ES",
                                        help="informe a sigla do Estado (UF) do endereço do Aluno",
                                        max_chars=2, key="novo_aluno_estado")

            self.st.button("salvar novo aluno", icon="💾", on_click=self.salvar)

            if "erros" in self.st.session_state and self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

    def exibir_lista_alunos(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Lista")
            self.st.button("novo aluno", on_click=self.ir_para_novo_aluno, icon="➕")
            alunos = self.aluno_db.listar()
            if len(alunos) == 0:
                self.st.write("nao ha alunos cadastrados")
            else:
                # aluno_com_colunas = pd.DataFrame(alunos, columns=["CPF", "Aluno", "Endereco"])
                self.st.dataframe(alunos)

    def exibir(self):
        if self.st.session_state.tela == "novo_aluno_sucesso":
            self.exibir_novo_aluno_sucesso()
        elif self.st.session_state.tela == "novo_aluno":
            self.exibir_novo_aluno()
        else:
            self.exibir_lista_alunos()
