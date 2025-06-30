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

    def cpf_ja_existe(self, cpf):
        registros = self.db.select(
            "SELECT cpf FROM aluno WHERE cpf = ?",
            (int(cpf),)
        )
        if not len(registros):
            return False
        registro_cpf = registros[0].get("cpf")
        cpf_ja_existe_valor = registro_cpf == int(cpf)
        return cpf_ja_existe_valor

    def cadastrar(self, aluno):
        self.db.executar(
            """
                INSERT INTO aluno(cpf, nome, ano_nascimento, email, endereco)
                VALUES(?, ?, ?, ?, ?)
            """,
            (int(aluno.cpf), aluno.nome, int(aluno.ano_nascimento), aluno.email, aluno.endereco)
        )
        self.db.confirmar()


if __name__ == "__main__":
    from banco_dados import BancoDados

    db = BancoDados("../../controle_academico.db")
    aluno_db = AlunoDB(db)

    # cpfs = db.executar("SELECT cpf FROM aluno")
    # print("OK ALUNO DB cpfs", [dict(cpf) for cpf in cpfs])

    # cpf_ja_existe = aluno_db.cpf_ja_existe("11111111111")
    # print("OK ALUNO DB cpf 11111111111 ja existe?", cpf_ja_existe)

    cpf_ja_existe = aluno_db.cpf_ja_existe("01234567890")
    print("TESTE ALUNO DB cpf 01234567890 ja existe?", cpf_ja_existe)

    cpf_ja_existe = aluno_db.cpf_ja_existe("1234567890")
    print("TESTE ALUNO DB cpf 1234567890 ja existe?", cpf_ja_existe)
