import requests


class Extract:
    """
    Classe responsável por realizar a extração de dados de diferentes APIs públicas.
    """

    def __init__(self):
        pass

    def extract_country(self, country):
        """
        Extrai dados de universidades de um país específico utilizando a API pública da Hipolabs.

        Args:
            country (str): O nome do país em inglês (ex: "Brazil", "Italy").

        Returns:
            list: Uma lista de dicionários contendo as informações das universidades.
        """
        url = f"http://universities.hipolabs.com/search?country={country}"
        response = requests.get(url)
        response.raise_for_status()
        universities = response.json()

        return universities

    def extract_meios_pagamentos(self, trimestre: str, n_retornos: str):
        """
        Extrai dados abertos sobre meios de pagamento trimestrais da API do Banco Central do Brasil.

        Args:
            trimestre (str): O trimestre e ano desejado no formato 'YYYYQ' (ex: '20251' para o 1º trimestre de 2025).
            n_retornos (str): O limite de registros que a API deve retornar (cláusula $top).

        Returns:
            dict: Um dicionário onde a chave 'value' contém a lista com os dados financeiros extraídos.
        """
        url = f"https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?@trimestre='{trimestre}'&$top={n_retornos}&$format=json&$select=datatrimestre,valorPix,valorCartaoCredito,valorCartaoDebito,quantidadePix,quantidadeCartaoCredito,quantidadeCartaoDebito"
        response = requests.get(url)
        response.raise_for_status()
        meios_pagamentos = response.json()

        return meios_pagamentos
    def extract_ibge_data(self):

        url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/202401/variaveis/4099?localidades=N3[26]&classificacao=2[6794]"

        try:

            response = requests.get(url)

            print("STATUS CODE:", response.status_code)

            print("RESPOSTA DA API:")
            print(response.text)

            response.raise_for_status()

            return response.json()

        except Exception as e:

            print(f"Erro na requisição: {e}")

            return None