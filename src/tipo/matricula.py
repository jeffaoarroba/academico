# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

from datetime import datetime
from util import eh_cpf_valido


class Matricula:
    """ Classe que representa uma Matricula de um Aluno em uma Disciplina """

    def __init__(self,
                 codigo_disciplina, cpf_aluno, matriculado_em=None,
                 nome_disciplina=None, carga_horaria_disciplina=None, nome_professor_disciplina=None,
                 nome_aluno=None, email_aluno=None, endereco_aluno=None):
        self.codigo_disciplina = int(
            codigo_disciplina) if codigo_disciplina else None
        self.cpf_aluno = int(cpf_aluno) if cpf_aluno else None
        self.matriculado_em = matriculado_em if matriculado_em else datetime.now()

        # Informacoes da disciplina
        self.nome_disciplina = nome_disciplina
        self.carga_horaria_disciplina = carga_horaria_disciplina
        self.nome_professor_disciplina = nome_professor_disciplina

        # Informacoes do aluno
        self.nome_aluno = nome_aluno
        self.email_aluno = email_aluno
        self.endereco_aluno = endereco_aluno

    def validar(self):
        """valida as informacoes da matricula e retorna os erros encontrados"""

        erros = []

        if not self.codigo_disciplina:
            erros.append("Informe o CODIGO da Disciplina")
        elif not self.codigo_disciplina > 0:
            erros.append(
                "O CODIGO da Disciplina deve ser um numero maior que zero")
        if not self.cpf_aluno:
            erros.append("Informe o CPF do Aluno")
        elif not eh_cpf_valido(self.cpf_aluno):
            erros.append("Informe um CPF válido do Aluno")

        return erros


if __name__ == "__main__":
    matricula1 = Matricula(
        codigo_disciplina=-10,
        cpf_aluno=""
    )
    print(matricula1.validar())
