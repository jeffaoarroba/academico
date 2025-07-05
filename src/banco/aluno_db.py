from tipo.aluno import Aluno


class AlunoDB:
    def __init__(self, db):
        self.db = db

    def listar(self):
        # https://www.sqlite.org/lang_datefunc.html
        #
        # no sqlite strftime('%Y', 'now') retorna o ano atual como string
        # CAST(strftime('%Y', 'now') AS INTEGER) converte o ano atual de string para numero para poder fazer operações matemáticas (como subtração)
        # ano_nascimento é o ano de nascimento do aluno
        # CAST(strftime('%Y', 'now') AS INTEGER) - ano_nascimento calcula a idade do aluno
        #
        # ORDER BY nome ASC ordena os alunos pelo nome em ordem alfabética
        #

        alunos = self.db.select(
            """
            SELECT
                cpf as CPF,
                nome as Nome,
                CAST(strftime('%Y', 'now') AS INTEGER) - ano_nascimento as Idade,
                email as Email,
                endereco as Endereco
            FROM aluno
            ORDER BY nome ASC
            """
        )
        return alunos

    def verificar_cpf_em_uso(self, cpf):
        if not cpf:
            return False

        registros = self.db.select(
            """
            SELECT cpf FROM aluno WHERE cpf = ?
            """,
            (int(cpf),)
        )

        if not len(registros):
            return False

        registro_cpf = registros[0].get("cpf")
        cpf_em_uso = registro_cpf == int(cpf)

        return cpf_em_uso

    def cadastrar(self, aluno: Aluno):
        self.db.executar(
            """
            INSERT INTO aluno(cpf, nome, ano_nascimento, email, endereco)
            VALUES(?, ?, ?, ?, ?)
            """,
            (
                int(aluno.cpf),
                aluno.nome,
                int(aluno.ano_nascimento),
                aluno.email,
                aluno.endereco
            )
        )
        self.db.confirmar()

    def excluir_por_cpf(self, cpf):
        if not cpf:
            return

        self.db.executar(
            """
            DELETE FROM aluno WHERE cpf = ?
            """,
            (int(cpf),)
        )

        self.db.confirmar()

    def obter_por_cpf(self, cpf):
        if not cpf:
            return None

        registros = self.db.select(
            """
            SELECT
                cpf,
                nome,
                ano_nascimento,
                CAST(strftime('%Y', 'now') AS INTEGER) - ano_nascimento as idade,
                email,
                endereco
            FROM aluno WHERE cpf = ?
            """,
            (int(cpf),)
        )

        if not len(registros):
            return None

        return Aluno(
            registros[0]["cpf"],
            registros[0]["nome"],
            registros[0]["ano_nascimento"],
            registros[0]["email"],
            registros[0]["endereco"]
        )

    def obter_nome_aluno_por_cpf(self, cpf):
        if not cpf:
            return None

        registros = self.db.select(
            """
            SELECT nome
            FROM aluno
            WHERE cpf = ?
            """,
            (int(cpf),)
        )

        if not len(registros):
            return None

        return registros[0]["nome"]

    def atualizar(self, aluno: Aluno):
        self.db.executar(
            """
            UPDATE aluno
            SET nome = ?, ano_nascimento = ?, email = ?, endereco = ?
            WHERE cpf = ?
            """,
            (
                aluno.nome,
                int(aluno.ano_nascimento),
                aluno.email,
                aluno.endereco,
                int(aluno.cpf)
            )
        )
        self.db.confirmar()
