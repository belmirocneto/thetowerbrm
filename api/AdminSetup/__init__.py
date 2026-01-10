import azure.functions as func
import logging

from shared.database import engine
from shared.models import Base, BattleReport

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Iniciando configuração do banco de dados...')

    try:
        Base.metadata.create_all(bind=engine)

        logging.info('Tabelas criadas/verificadas com sucesso.')

        return func.HttpResponse(
            "Database setup completed successfully. Tables are ready.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Erro ao configurar o banco: {str(e)}")
        return func.HttpResponse(
            f"Error during database setup: {str(e)}",
            status_code=500
        )