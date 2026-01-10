import azure.functions as func
import logging
import traceback # Para ver o rastro do erro
import sys
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Iniciando AdminSetup...')
    
    try:
        # 1. Tentar importar as dependências dentro do try para capturar erro de módulo
        from shared.database import engine
        from shared.models import Base, BattleReport
        
        logging.info('Criando tabelas...')
        Base.metadata.create_all(bind=engine)
        
        return func.HttpResponse("Sucesso! Tabelas criadas.", status_code=200)

    except Exception as e:
        # 2. Captura o erro detalhado e o rastro (stack trace)
        error_stack = traceback.format_exc()
        logging.error(f"Erro detalhado:\n{error_stack}")
        
        return func.HttpResponse(
            f"Erro no Setup:\n{str(e)}\n\nStack Trace:\n{error_stack}",
            status_code=500
        )