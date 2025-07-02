class Disciplina:

    def __init__(self, nome, carga_horaria, nome_professor):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.nome_professor = nome_professor

    def validar(self):
        """valida as informacoes da disciplina e retorna os erros encontrados"""
        erros = []

        """TODO: validar quando o valor tiver somente espacos, ex: nome='  '"""

        if not self.nome:
            erros.append("Informe o nome da Disciplina")
        if not self.carga_horaria:
            erros.append("Informe a carga horaria da Disciplina")
        elif self.carga_horaria <= 0:
            erros.append("A carga horaria da Disciplina deve ser um valor maior que zero")
        if not self.nome_professor:
            erros.append("Informe o nome do professor da Disciplina")

        return erros

if __name__ == "__main__":
    disciplina1 = Disciplina(
        nome="Portugues",
        carga_horaria=-10,
        nome_professor="Prefessor Nome"
    )
    print (disciplina1.validar())
