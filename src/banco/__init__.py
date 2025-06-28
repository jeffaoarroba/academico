from .banco_dados import BancoDados
from .aluno_db import AlunoDB

db = BancoDados()
db.criar_tabelas()

aluno_db = AlunoDB(db)

__all__ = ["aluno_db"]