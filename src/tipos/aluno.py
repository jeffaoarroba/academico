class Aluno:

    def __init__(self, cpf, nome, ano_nascimento, email, endereco):
        self.cpf = 0
        self.ano_nascimento = 0

        if cpf:
            self.cpf = int(cpf)
        if ano_nascimento:
            self.ano_nascimento = int(ano_nascimento)

        self.nome = nome.upper()
        self.email = email.upper()
        self.endereco = endereco.upper()

    def validar(self):
        """ valida as informacoes do aluno e retorna os erros encontrados """
        erros = []

        if not self.cpf:
            erros.append("🪪 Informe o **CPF** do Aluno")
        elif not self.validarCPF(self.cpf):
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

    def validarCPF(self, cpf):
        ### Recebe uma string com o CPF,
        # extrai os 9 primeiros dígitos do CPF
        # e calcula os dois ultimos dígitos verificadores
        # refencia https://pt.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas#Algoritmo

        ### preparacao
        # preenche com zeros a esquerda um CPF que tenha menos de 11 digitos
        cpf_com_onze_digitos = str(cpf).zfill(11)
        # pega os 9 primeiros digitos para fazer o calculo dos dois ultimos digitos verificacores
        cpf_primeiro_nove_digitos = cpf_com_onze_digitos[:9]
        # inverte a posicao dos digitos do CPF, util para simplificar o calculo que sera feito na proxima etapa
        cpf_invertido = []
        indice = len(cpf_primeiro_nove_digitos) - 1
        while indice >= 0:
            digito = cpf_primeiro_nove_digitos[indice]
            cpf_invertido.append(int(digito))
            indice -= 1

        ### digitos verificadores
        dv1 = 0  # digito verificador 1, valor inicial
        dv2 = 0  # digito verificador 2, valor inicial
        # calcula o dois digitos verificadores
        for i in range(len(cpf_invertido)):
            dv1 += cpf_invertido[i] * (9 - (i % 10))
            dv2 += cpf_invertido[i] * (9 - ((i + 1) % 10))
        # calcula os dois últimos dígitos do CPF
        dv1 = (dv1 % 11) % 10
        dv2 += dv1 * 9
        dv2 = (dv2 % 11) % 10
        ### compara e valida
        # os dois ultimos digitos do CPF informados
        # com os dois ultimos digitos do CPF calculados
        dv1_str = str(dv1)
        dv2_str = str(dv2)
        cpf_valido = cpf_com_onze_digitos[9] == dv1_str and cpf_com_onze_digitos[10] == dv2_str
        if not cpf_valido:
            print("ERRO ALUNO validar CPF", cpf_com_onze_digitos, "DV1", dv1, "DV2", dv2)
        return cpf_com_onze_digitos[11 - 2] == str(dv1) and cpf_com_onze_digitos[11 - 1] == str(dv2)


"""
curiosidade CPF com 11 digitos com o mesmo valor sao CPFs validos, exemplo
00000000000
11111111111
22222222222
33333333333
44444444444
55555555555
...
pois passam com sucesso na validacao e no calculo dos digitos verificadores,
outra sequencia simples que passa na validacao do CPF
01234567890
"""

if __name__ == "__main__":
    aluno1 = Aluno("01234567890", "JEUDI", 1985, "jeudiprando@gmail.com", "Centro, Domingos Martins - ES")
    print(aluno1.validar())
