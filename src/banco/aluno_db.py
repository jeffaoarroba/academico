class AlunoDB:
    def __init__(self, db):
        self.db = db

    def listar(self):
        registros = self.db.executar(
            "SELECT cpf as CPF, nome as Nome, endereco as Endereco FROM aluno ORDER BY nome ASC")
        lista_alunos = []
        for linha in registros:
            aluno = dict(linha)
            lista_alunos.append(aluno)
        return lista_alunos

    def cadastrar(self, aluno):
        self.db.executar(
            """
                INSERT INTO aluno(cpf, nome, ano_nascimento, email, endereco)
                VALUES(?, ?, ?, ?, ?)
            """,
            (aluno.cpf, aluno.nome, aluno.ano_nascimento, aluno.email, aluno.endereco)
        )
