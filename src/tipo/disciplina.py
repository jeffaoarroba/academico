class Disciplina:
    """ Classe que representa uma Disciplina """

    def __init__(self, nome, carga_horaria, nome_professor, codigo=None):
        self.codigo = int(codigo) if codigo else None
        self.nome = nome.upper()
        self.carga_horaria = int(carga_horaria)
        self.nome_professor = nome_professor.upper()

    def validar(self):
        """valida as informacoes da disciplina e retorna os erros encontrados"""
        erros = []

        if self.codigo and self.codigo <= 0:
            erros.append("🪪 O **CODIGO** da Disciplina informado é invalido!")
        if not self.nome:
            erros.append("📘 Informe o **NOME** da Disciplina")
        if not self.carga_horaria:
            erros.append("⏳ Informe a **CARGA HORARIA** da Disciplina")
        elif self.carga_horaria <= 0:
            erros.append(
                "⏳ A **CARGA HORARIA** da Disciplina deve ser um valor maior que zero")
        if not self.nome_professor:
            erros.append("👨‍🏫 Informe o **PROFESSOR** da Disciplina")

        return erros


if __name__ == "__main__":
    disciplina1 = Disciplina(
        nome="Portugues",
        carga_horaria=-10,
        nome_professor="Prefessor Nome"
    )
    print(disciplina1.validar())
