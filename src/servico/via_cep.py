import requests
import json

# https://docs.python.org/pt-br/3.13/library/stdtypes.html#str.join
# https://docs.python.org/pt-br/3.13/library/functions.html#filter
# https://www.digitalocean.com/community/tutorials/how-to-use-the-python-filter-function-pt#como-usar-none-com-filter


class ViaCEP:
    def __init__(self, cep):
        self.cep = cep

    def obter_endereco_completo(self):
        """
            https://viacep.com.br/ws/CEP/json/
            Faz uma requisição HTTP para a API ViaCEP, busca o endereço
            e retorna uma string formatada com o endereço completo.
        """

        if len(self.cep) != 8:
            return {"erro": "O CEP informado não é válido!"}

        url = f"https://viacep.com.br/ws/{self.cep}/json/"

        try:
            # faz uma requisicao http, solicitando as informacoes do CEP, para o servico viacep
            response = requests.get(url)
            # gera um erro se o status da requisicao nao for OK (sucesso)
            response.raise_for_status()
            # le a resposta (da requisicao) com as informacoes do CEP
            data = response.json()

            if 'erro' in data and data['erro']:
                print("ERRO SERVICO CEP", self.cep, "não encontrado.")
                return {"erro": "CEP '" + self.cep + "' não encontrado."}

            # informacoes do endereco
            logradouro = data.get('logradouro', '')
            bairro = data.get('bairro', '')
            localidade = data.get('localidade', '')
            uf = data.get('uf', '')

            return {
                "erro": False,
                # "endereco_completo": logradouro + ", " + bairro + ", " + localidade + "-" + uf + " CEP:" + self.cep
                "endereco_completo": ", ".join(list(filter(None, [
                    logradouro,
                    bairro,
                    localidade,
                    uf,
                    "CEP:" + self.cep
                ])))
            }
        except Exception as e:
            print("ERRO SERVICO CEP Ocorreu um erro inesperado", e)
            return {"erro": "Ocorreu um erro inesperado"}


if __name__ == "__main__":
    endereco_completo = ViaCEP("29171131").obter_endereco_completo()
    print("endereco:", endereco_completo)
