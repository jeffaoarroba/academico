from datetime import datetime

class Matricula:

    def __init__(self, codigo_disciplina, cpf_aluno):
        self.codigo_disciplina = codigo_disciplina
        self.cpf_aluno = cpf_aluno
        self.matriculado_em = datetime.now()

    def validar(self):
        """valida as informacoes da matricula e retorna os erros encontrados"""
        erros = []

        if not self.codigo_disciplina:
            erros.append("Informe o codigo da disciplina da Matricula")
        elif self.codigo_disciplina <= 0:
            erros.append("O codigo da disciplina da Matricula deve ser um valor maior que zero")
        if not self.cpf_aluno:
            erros.append("Informe o CPF do aluno da Disciplina")
        """TODO: validar o CPF do aluno, se eh um CPF valido"""

        return erros


if __name__ == "__main__":
    matricula1 = Matricula(
        codigo_disciplina=-10,
        cpf_aluno=""
    )
    print(matricula1.validar())
