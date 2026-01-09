import azure.functions as func
import json
import logging
import os
import sys
from pathlib import Path

# Adicionar diretório pai ao path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

try:
    from shared.database import get_db
    from shared.models import BattleReport
    from shared.auth import validate_api_key, validate_user_id
except ImportError as e:
    logging.error(f"Import error: {e}")
    logging.error(f"Python path: {sys.path}")
    raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('--- DEBUG: MINHA FUNCAO NOVA ESTA RODANDO ---')
    logging.info('GetReports function triggered')

    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',  # Temporário para teste
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
        'Content-Type': 'application/json'
    }

    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return func.HttpResponse(status_code=204, headers=headers)

    try:
        # Validar API Key
        is_valid, error_msg = validate_api_key(req)
        if not is_valid:
            return func.HttpResponse(
                json.dumps({'error': error_msg}),
                status_code=401,
                headers=headers
            )

        # Pegar parâmetros
        user_id = req.params.get('user_id')
        limit = int(req.params.get('limit', 15))
        page = int(req.params.get('page', 1))

        # Validar user_id
        is_valid, error_msg = validate_user_id(user_id)
        if not is_valid:
            return func.HttpResponse(
                json.dumps({'error': error_msg}),
                status_code=400,
                headers=headers
            )

        db = get_db()
        offset = (page - 1) * limit

        reports = db.query(BattleReport)\
            .filter_by(user_id=user_id)\
            .order_by(BattleReport.battle_date.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()

        reports_data = [r.to_dict() for r in reports]

        db.close()

        return func.HttpResponse(
            json.dumps({'reports': reports_data}),
            status_code=200,
            headers=headers
        )

    except Exception as e:
        logging.error(f'Error in GetReports: {str(e)}')
        import traceback
        logging.error(traceback.format_exc())

        return func.HttpResponse(
            json.dumps({'error': f'Internal server error: {str(e)}'}),
            status_code=500,
            headers=headers
        )