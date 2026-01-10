import azure.functions as func
import logging
import sys
import os

# Forçar o log a aparecer no Log Stream
logging.info("Tentando carregar o módulo AdminSetup")

try:
    from shared.database import engine
    from shared.models import Base, BattleReport
    logging.info("Dependências carregadas com sucesso no AdminSetup")
except Exception as e:
    logging.error(f"FALHA NO IMPORT DO ADMINSETUP: {str(e)}")