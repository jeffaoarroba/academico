class Aluno:

    def __init__(self, cpf, nome, ano_nascimento, email, endereco):
        self.cpf = cpf
        self.nome = nome
        self.ano_nascimento = ano_nascimento
        self.email = email
        self.endereco = endereco

    def validar(self):
        """valida as informacoes do aluno e retorna os erros encontrados"""
        erros = []

        if not self.nome:
            erros.append("Informe o nome do Aluno")
        if not self.ano_nascimento:
            erros.append("Informe o ano da data de nascimento do Aluno")
        elif self.ano_nascimento <= 1970:
            erros.append("O ano da data de nascimento do Aluno nao pode ser inferior a 1970")
        if not self.email:
            erros.append("Informe o email do Aluno")
        if not self.endereco:
            erros.append("Informe o endereço do Aluno")

        return erros

if __name__ == "__main__":
    aluno1 = Aluno("110","","","","")
    print (aluno1.validar())
