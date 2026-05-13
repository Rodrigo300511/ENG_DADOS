def transform_data(data):

    if data is None:
        raise ValueError("Nenhum dado foi retornado pela API")

    resultado = []

    try:

        serie = data[0]["resultados"][0]["series"][0]["serie"]

        for periodo, valor in serie.items():

            documento = {
                "periodo": periodo,
                "valor": float(valor)
            }

            resultado.append(documento)

        return resultado

    except Exception as e:

        raise Exception(f"Erro na transformação dos dados: {e}")