from datetime import datetime
from banco.aluno_db import AlunoDB
from tipos.aluno import Aluno
from servico.via_cep import ViaCEP


class AlunoApp:

    def __init__(self, st, placeholder, aluno_db: AlunoDB):
        self.st = st
        self.placeholder = placeholder
        self.aluno_db = aluno_db

    def obter_novo_aluno(self):
        if self.st.session_state.novo_aluno_cep_erro:
            self.st.session_state.novo_aluno_endereco = ", ".join(list(filter(None, [
                self.st.session_state.novo_aluno_logradouro,
                self.st.session_state.novo_aluno_bairro,
                self.st.session_state.novo_aluno_cidade,
                self.st.session_state.novo_aluno_estado,
                "CEP:" + self.st.session_state.novo_aluno_cep
            ])))
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
        cpf_ja_existe = self.aluno_db.verificar_cpf_em_uso(novo_aluno.cpf)
        if cpf_ja_existe:
            erros.insert(0, "🪪 O **CPF** informado já está sendo utilizado")
        if not erros:
            self.aluno_db.cadastrar(novo_aluno)
            self.st.session_state.tela = "novo_aluno_sucesso"
        self.st.session_state.erros = erros

    def ir_para_lista_alunos(self):
        self.st.session_state.menu = "Alunos"
        self.st.session_state.tela = "lista_alunos"

    def ir_para_novo_aluno(self):
        self.st.session_state.novo_aluno_cep_erro = False
        self.st.session_state.novo_aluno_endereco = ""
        self.st.session_state.menu = "Alunos"
        self.st.session_state.tela = "novo_aluno"

    def exibir_novo_aluno_sucesso(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno")
            self.st.button("voltar", on_click=self.ir_para_lista_alunos,
                           help="voltar para a listagem de alunos")
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
            self.st.button("voltar", on_click=self.ir_para_lista_alunos,
                           help="**cancelar** o cadastro do novo aluno e voltar para a listagem de alunos")
            self.st.write("Informe os dados do novo Aluno")

            self.st.text_input("CPF:", max_chars=11, placeholder="informe somente os numeros do CPF",
                               icon="🪪",
                               key="novo_aluno_cpf")
            self.st.text_input("Nome:", max_chars=200,
                               placeholder="informe o nome completo do novo aluno",
                               icon="🧑", key="novo_aluno_nome")
            self.st.number_input("Ano de Nascimento:", value=None, min_value=1970,
                                 max_value=datetime.now().year - 1,
                                 help="se a data de nascimento do Aluno é 01/02/2003, informe somente o ano 2003",
                                 placeholder="informe somente o ANO da data de nascimento do Aluno",
                                 icon="🗓️", key="novo_aluno_ano")
            self.st.text_input("Email:", max_chars=200,
                               icon="✉️", key="novo_aluno_email")

            self.st.text_input("CEP:", placeholder="informe somente os numeros do CEP", max_chars=200,
                               icon="🛣️", key="novo_aluno_cep")

            clicou_em_consultar_cep = self.st.button("consultar CEP", icon="🔎")

            if clicou_em_consultar_cep:
                self.st.session_state.novo_aluno_cep_erro = False
                self.st.session_state.novo_aluno_endereco = ""
                try:
                    if self.st.session_state.novo_aluno_cep:
                        print("APP ALUNO consultar_cep",
                              self.st.session_state.novo_aluno_cep)
                        consulta_cep = ViaCEP(
                            self.st.session_state.novo_aluno_cep).obter_endereco_completo()
                        if consulta_cep['erro']:
                            print("ERRO APP ALUNO consultar_cep",
                                  consulta_cep['erro'])
                            self.st.session_state.novo_aluno_cep_erro = consulta_cep['erro']
                        else:
                            self.st.session_state.novo_aluno_endereco = consulta_cep['endereco_completo']
                            print("APP ALUNO endereco_completo",
                                  consulta_cep['endereco_completo'])
                            # self.st.write(consulta_cep['endereco_completo'])
                    else:
                        print("APP ALUNO cep não informado")
                        self.st.session_state.novo_aluno_cep_erro = "CEP não informado"
                except Exception as e:
                    print("ERRO APP ALUNO consultar_cep", e)
                    self.st.session_state.novo_aluno_cep_erro = e

            if self.st.session_state.novo_aluno_endereco:
                self.st.text_input("Endereço", disabled=True,
                                   value=self.st.session_state.novo_aluno_endereco)

            if self.st.session_state.novo_aluno_cep_erro:
                self.st.error(self.st.session_state.novo_aluno_cep_erro)

                self.st.text_input("Logradouro:", placeholder="rua Canela, 110", max_chars=200,
                                   key="novo_aluno_logradouro")
                self.st.text_input("Bairro:", placeholder="Centro", max_chars=200,
                                   key="novo_aluno_bairro")
                self.st.text_input("Cidade:", placeholder="Serra", max_chars=200,
                                   key="novo_aluno_cidade")
                self.st.text_input("Estado:", placeholder="ES",
                                   help="informe a sigla do Estado (UF) do endereço do Aluno",
                                   max_chars=2, key="novo_aluno_estado")

            self.st.button("salvar novo aluno", icon="💾", on_click=self.salvar)

            if "erros" in self.st.session_state and self.st.session_state.erros:
                for erro in self.st.session_state.erros:
                    self.st.error(erro)
                self.st.session_state.erros = None

            # debug global
            # self.st.write(self.st.session_state)

    def exibir_lista_alunos(self):
        with self.placeholder.container():
            self.st.subheader("🧑‍🎓 Aluno | Lista")
            self.st.button(
                "novo aluno", on_click=self.ir_para_novo_aluno, icon="➕")
            alunos = self.aluno_db.listar()
            if len(alunos) == 0:
                self.st.write("nao ha alunos cadastrados")
            else:
                self.st.dataframe(alunos)

    def exibir(self):
        if self.st.session_state.tela == "novo_aluno_sucesso":
            self.exibir_novo_aluno_sucesso()
        elif self.st.session_state.tela == "novo_aluno":
            self.exibir_novo_aluno()
        else:  # lista_alunos
            self.exibir_lista_alunos()
