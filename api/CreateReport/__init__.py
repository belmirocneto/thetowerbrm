import azure.functions as func
import json
import logging
import sys
from pathlib import Path

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

try:
    from shared.database import get_db
    from shared.models import BattleReport
    from shared.auth import validate_api_key, validate_user_id
    from shared.parser import parse_battle_report
except ImportError as e:
    logging.error(f"Import error: {e}")
    raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CreateReport function triggered')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
        'Content-Type': 'application/json'
    }

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

        body = req.get_json()
        raw_data = body.get('raw_data', '')
        user_id = body.get('user_id', '')

        # Validar user_id
        is_valid, error_msg = validate_user_id(user_id)
        if not is_valid:
            return func.HttpResponse(
                json.dumps({'error': error_msg}),
                status_code=400,
                headers=headers
            )

        if not raw_data:
            return func.HttpResponse(
                json.dumps({'error': 'raw_data is required'}),
                status_code=400,
                headers=headers
            )

        # Parse do report
        parsed_data = parse_battle_report(raw_data)

        if not parsed_data:
            return func.HttpResponse(
                json.dumps({'error': 'Failed to parse battle report'}),
                status_code=400,
                headers=headers
            )

        parsed_data['user_id'] = user_id

        # Salvar no banco
        db = get_db()
        report = BattleReport(**parsed_data)
        db.add(report)
        db.commit()

        report_id = report.id
        db.close()

        return func.HttpResponse(
            json.dumps({
                'message': 'Report saved successfully',
                'id': report_id
            }),
            status_code=201,
            headers=headers
        )

    except Exception as e:
        logging.error(f'Error in CreateReport: {str(e)}')
        import traceback
        logging.error(traceback.format_exc())

        return func.HttpResponse(
            json.dumps({'error': f'Internal server error: {str(e)}'}),
            status_code=500,
            headers=headers
        )