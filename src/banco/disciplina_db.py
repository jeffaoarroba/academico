# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

from tipo.disciplina import Disciplina


class DisciplinaDB:
    def __init__(self, db):
        self.db = db

    def listar(self):
        """ Retorna uma lista de todas as disciplinas cadastradas no banco de dados."""

        disciplinas = self.db.select(
            """
            SELECT
                codigo as Codigo,
                nome as Nome,
                carga_horaria as CargaHoraria,
                nome_professor as Professor
            FROM disciplina
            ORDER BY nome ASC
            """
        )

        return disciplinas

    def verificar_codigo_em_uso(self, codigo_disciplina):
        if not codigo_disciplina:
            return False

        if isinstance(codigo_disciplina, str) and not codigo_disciplina.isdigit():
            return False

        registros = self.db.select(
            """
            SELECT codigo FROM disciplina WHERE codigo = ?
            """,
            (int(codigo_disciplina),)
        )

        if not len(registros):
            return False

        registro_codigo_disciplina = registros[0].get("codigo")
        codigo_em_uso = registro_codigo_disciplina == int(codigo_disciplina)

        return codigo_em_uso

    def cadastrar(self, disciplina: Disciplina):
        lista = self.db.executar(
            """
            INSERT INTO disciplina(nome, carga_horaria, nome_professor)
            VALUES(?, ?, ?)
            RETURNING codigo
            """,
            (
                disciplina.nome,
                int(disciplina.carga_horaria),
                disciplina.nome_professor,
            )
        )
        self.db.confirmar()
        return lista[0]["codigo"] if lista else None

    def excluir_por_codigo(self, codigo_disciplina):
        if not codigo_disciplina:
            return

        self.db.executar(
            """
            DELETE FROM disciplina WHERE codigo = ?
            """,
            (int(codigo_disciplina),)
        )

        self.db.confirmar()

    def obter_por_codigo(self, codigo_disciplina):
        if not (codigo_disciplina):
            return None

        registros = self.db.select(
            """
            SELECT
                codigo as Codigo,
                nome as Nome,
                carga_horaria as CargaHoraria,
                nome_professor as Professor
            FROM disciplina
            WHERE codigo = ?
            """,
            (int(codigo_disciplina),)
        )

        if not len(registros):
            return None

        return Disciplina(
            registros[0]["Nome"],
            registros[0]["CargaHoraria"],
            registros[0]["Professor"],
            registros[0]["Codigo"]
        )

    def obter_nome_disciplina_por_codigo(self, codigo_disciplina):
        if not (codigo_disciplina):
            return None

        registros = self.db.select(
            """
            SELECT nome
            FROM disciplina
            WHERE codigo = ?
            """,
            (int(codigo_disciplina),)
        )

        if not len(registros):
            return None

        return registros[0]["nome"]

    def atualizar(self, disciplina: Disciplina):
        self.db.executar(
            """
            UPDATE disciplina
            SET nome = ?, carga_horaria = ?, nome_professor = ?
            WHERE codigo = ?
            """,
            (
                disciplina.nome,
                int(disciplina.carga_horaria),
                disciplina.nome_professor,
                int(disciplina.codigo)
            )
        )
        self.db.confirmar()
