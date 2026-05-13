from prefect import flow, task, get_run_logger

from src.extract import Extract
from src.transform import transform_data
from src.load import Load


@task(
    name="EXTRACT_IBGE",
    retries=3,
    retry_delay_seconds=5
)
def extract_task():

    logger = get_run_logger()

    logger.info("Iniciando extração dos dados do IBGE")

    extractor = Extract()

    data = extractor.extract_ibge_data()

    if data is None:

        logger.error("Falha na extração dos dados da API do IBGE")

        raise ValueError("A extração retornou None")

    logger.info("Dados extraídos com sucesso")

    return data


@task(name="TRANSFORM_IBGE")
def transform_task(data):

    logger = get_run_logger()

    logger.info("Iniciando transformação dos dados")

    transformed_data = transform_data(data)

    logger.info(
        f"{len(transformed_data)} registros transformados com sucesso"
    )

    return transformed_data


@task(name="LOAD_MONGODB")
def load_task(data):

    logger = get_run_logger()

    logger.info("Iniciando carga no MongoDB")

    loader = Load()

    loader.insert_in_mongo(
        data,
        "ibge_db",
        "taxa_desemprego"
    )

    logger.info(
        f"{len(data)} registros inseridos no MongoDB com sucesso"
    )


@flow(
    name="ETL_IBGE",
    log_prints=True
)
def etl_flow():

    logger = get_run_logger()

    logger.info("Pipeline ETL iniciado")

    dados_brutos = extract_task()

    dados_transformados = transform_task(dados_brutos)

    load_task(dados_transformados)

    logger.info("Pipeline ETL finalizado com sucesso")


if __name__ == "__main__":

    etl_flow()