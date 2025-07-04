from .banco_dados import BancoDados
from .aluno_db import AlunoDB
from .disciplina_db import DisciplinaDB

db = BancoDados()
db.criar_tabelas()

aluno_db = AlunoDB(db)
disciplina_db = DisciplinaDB(db)

__all__ = ["aluno_db", "disciplina_db"]
