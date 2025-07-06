# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

from .banco_dados import BancoDados
from .aluno_db import AlunoDB
from .disciplina_db import DisciplinaDB
from .matricula_db import MatriculaDB

db = BancoDados()
db.criar_tabelas()

aluno_db = AlunoDB(db)
disciplina_db = DisciplinaDB(db)
matricula_db = MatriculaDB(db)

__all__ = ["aluno_db", "disciplina_db", "matricula_db"]
