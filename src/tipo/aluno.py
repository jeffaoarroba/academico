from datetime import datetime
from util import eh_cpf_valido


class Aluno:
    """ Classe que representa um Aluno """

    def __init__(self, cpf, nome, ano_nascimento, email, endereco):
        self.cpf = 0
        self.ano_nascimento = 0
        self.idade = 0

        if cpf:
            self.cpf = int(cpf)
        if ano_nascimento:
            self.ano_nascimento = int(ano_nascimento)
            # SE o ano de nascimento for informado,
            # calcula a idade do aluno
            self.idade = datetime.now().year - self.ano_nascimento

        self.nome = nome.upper()
        self.email = email.upper()
        self.endereco = endereco.upper()

    def validar(self):
        """ valida as informacoes do aluno e retorna os erros encontrados """
        erros = []

        if not self.cpf:
            erros.append("🪪 Informe o **CPF** do Aluno")
        elif not eh_cpf_valido(self.cpf):
            erros.append("🪪 O **CPF** informado não é válido")
        if not self.nome:
            erros.append("🧑 Informe o **NOME** do Aluno")
        if not self.ano_nascimento:
            erros.append("🗓️ Informe o **ANO** da data de nascimento do Aluno")
        if not self.email:
            erros.append("✉️ Informe o **EMAIL** do Aluno")
        if not self.endereco:
            erros.append("🛣️ Informe o **ENDEREÇO** do Aluno")

        return erros


if __name__ == "__main__":
    aluno1 = Aluno("01234567890", "JEUDI", 1985,
                   "jeudiprando@gmail.com", "Centro, Domingos Martins - ES")
    print(aluno1.validar())
