from tipo.aluno import Aluno


class AlunoDB:
    def __init__(self, db):
        self.db = db

    def listar(self):
        alunos = self.db.select(
            """
            SELECT cpf as CPF, nome as Nome, endereco as Endereco
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
                cpf as CPF,
                nome as Nome,
                ano_nascimento as AnoNascimento,
                email as Email,
                endereco as Endereco
            FROM aluno WHERE cpf = ?
            """,
            (int(cpf),)
        )

        if not len(registros):
            return None

        return Aluno(
            registros[0]["CPF"],
            registros[0]["Nome"],
            registros[0]["AnoNascimento"],
            registros[0]["Email"],
            registros[0]["Endereco"]
        )

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
