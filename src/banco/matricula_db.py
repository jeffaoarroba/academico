from tipo.matricula import Matricula


class MatriculaDB:
    """ Classe que representa o banco de dados de Matriculas """

    """
    O campo matriculado_em armazena a data e hora em que a matricula foi realizada.
    É sempre armazenado no formato UTC (Coordinated Universal Time).
    O fuso horário UTC-3 (horário de Brasília) é aplicado ao exibir as datas e horas
    para que os usuários vejam a data e hora corretamente.
    """

    def __init__(self, db):
        self.db = db

    def listar(self):
        """ Retorna uma lista de todas as matriculas cadastradas no banco de dados."""

        matriculas = self.db.select(
            """
            SELECT
                strftime('%d/%m/%Y %H:%M', datetime(matriculado_em, '-3 hours')) AS matriculado_em,
                codigo_disciplina,
                disciplina.nome AS nome_disciplina,
                cpf_aluno,
                aluno.nome AS nome_aluno
            FROM matricula
            JOIN disciplina ON disciplina.codigo = codigo_disciplina
            JOIN aluno ON aluno.cpf = cpf_aluno
            ORDER BY aluno.nome, disciplina.nome
            """
        )
        # exemplo:
        # o campo matriculado_em com o valor: 2025-07-05 19:05:00
        # em UTC eh exibido: 05/07/2025 19:05
        # em UTC-3 eh exibido: 05/07/2025 16:05

        return matriculas

    def verificar_em_uso(self, codigo_disciplina, cpf_aluno):
        """ Verifica se uma matricula está em uso pelo código da disciplina e CPF do aluno. """

        if not codigo_disciplina or not cpf_aluno:
            return False

        registros = self.db.select(
            """
            SELECT matriculado_em FROM matricula WHERE codigo_disciplina = ? AND cpf_aluno = ?
            """,
            (int(codigo_disciplina), int(cpf_aluno))
        )

        if not len(registros):
            return False

        estah_em_uso = registros[0].get("matriculado_em")
        if not estah_em_uso:
            return False

        return True

    def cadastrar(self, matricula: Matricula):
        """ Cadastra uma nova matricula no banco de dados. """

        lista = self.db.executar(
            """
            INSERT INTO matricula(codigo_disciplina, cpf_aluno)
            VALUES(?, ?)
            RETURNING matriculado_em
            """,
            (
                int(matricula.codigo_disciplina),
                int(matricula.cpf_aluno),
            )
        )
        self.db.confirmar()
        return lista[0]["matriculado_em"] if lista else None

    def excluir_por(self, codigo_disciplina, cpf_aluno):
        """ Exclui uma matricula pelo código da disciplina e CPF do aluno. """

        if not codigo_disciplina or not cpf_aluno:
            return

        self.db.executar(
            """
            DELETE FROM matricula WHERE codigo_disciplina = ? AND cpf_aluno = ?
            """,
            (int(codigo_disciplina), int(cpf_aluno))
        )

        self.db.confirmar()

    def obter_por(self, codigo_disciplina, cpf_aluno):
        """ Obtém uma matricula pelo código da disciplina e CPF do aluno. """

        if not codigo_disciplina or not cpf_aluno:
            return None

        registros = self.db.select(
            """
            SELECT
                matriculado_em,
                codigo_disciplina,
                disciplina.nome AS nome_disciplina,
                disciplina.carga_horaria AS carga_horaria_disciplina,
                disciplina.nome_professor AS nome_professor_disciplina,
                cpf_aluno,
                aluno.nome AS nome_aluno,
                email AS email_aluno,
                endereco AS endereco_aluno
            FROM matricula
            JOIN disciplina ON disciplina.codigo = codigo_disciplina
            JOIN aluno ON aluno.cpf = cpf_aluno
            WHERE codigo_disciplina = ? AND cpf_aluno = ?
            """,
            (int(codigo_disciplina), int(cpf_aluno))
        )

        if not len(registros):
            return None

        return Matricula(
            registros[0]["codigo_disciplina"],
            registros[0]["cpf_aluno"],
            registros[0]["matriculado_em"],
            registros[0]["nome_disciplina"],
            registros[0]["carga_horaria_disciplina"],
            registros[0]["nome_professor_disciplina"],
            registros[0]["nome_aluno"],
            registros[0]["email_aluno"],
            registros[0]["endereco_aluno"]
        )
