# Projeto: Sistema de Controle Acadêmico
# Desenvolvedor: Jefferson Gonçalves Andrade

def gerar_endereco_completo(logradouro, bairro, cidade, uf, cep):
    """
    Gera o endereço completo.
    """

    # cria uma lista com logradouro, bairro, cidade
    # remove os valores vazios e junta os valores com vírgula,
    # e transforma os valores em letras maiúsculas.
    endereco = ", ".join(list(filter(None, [
        logradouro if logradouro else None,
        bairro if bairro else None,
        cidade if cidade else None,
    ]))).strip(", ").strip()

    # concatena o valor gerado anteriormente com uf e cep
    # se uf e cep forem informados, adiciona um separador
    endereco_completo = endereco + (" - " if endereco and uf else "") + (
        uf if uf else "") + (" CEP:" + cep if cep else "")

    # e retorna um valor com o endereço completo.
    return endereco_completo.upper()


def eh_cpf_valido(cpf):
    """
    Valida um CPF (Cadastro de Pessoas Físicas) brasileiro.
    """

    # Recebe uma string com o CPF,
    # extrai os 9 primeiros dígitos do CPF
    # e calcula os dois ultimos dígitos verificadores
    # refencia https://pt.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas#Algoritmo

    # PREPARACAO
    print("UTIL eh_cpf_valido", cpf)

    if not cpf:
        print("ERRO UTIL eh_cpf_valido CPF vazio")
        return False

    if not cpf.isdigit():
        print("ERRO UTIL eh_cpf_valido", cpf, "isdigit False")
        return False

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

    # DIGITOS VERIFICADORES
    digito_verificador1 = 0  # digito verificador 1, valor inicial
    digito_verificador2 = 0  # digito verificador 2, valor inicial

    # calcula o dois digitos verificadores
    for i in range(len(cpf_invertido)):
        digito_verificador1 += cpf_invertido[i] * (9 - (i % 10))
        digito_verificador2 += cpf_invertido[i] * (9 - ((i + 1) % 10))

    # calcula os dois últimos dígitos do CPF
    digito_verificador1 = (digito_verificador1 % 11) % 10
    digito_verificador2 += digito_verificador1 * 9
    digito_verificador2 = (digito_verificador2 % 11) % 10

    # COMPARA E VALIDA
    # os dois ultimos digitos do CPF informados
    # com os dois ultimos digitos do CPF calculados
    eh_cpf_valido = cpf_com_onze_digitos[9] == str(
        digito_verificador1) and cpf_com_onze_digitos[10] == str(digito_verificador2)

    if not eh_cpf_valido:
        print("ERRO UTIL eh_cpf_valido",
              cpf_com_onze_digitos, "DV1", digito_verificador1, "DV2", digito_verificador2)

    return eh_cpf_valido


__all__ = ["eh_cpf_valido", "gerar_endereco_completo"]

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
