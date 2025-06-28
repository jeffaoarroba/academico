class AlunoDB:
    def __init__(self, db):
        self.db = db

    def listar_alunos(self):
        alunos = self.db.executar("SELECT cpf, nome, endereco FROM aluno ORDER BY nome ASC")
        return alunos
