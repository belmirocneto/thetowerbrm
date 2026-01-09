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
except ImportError as e:
    logging.error(f"Import error: {e}")
    raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DeleteReport function triggered')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
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

        report_id = req.route_params.get('report_id')
        user_id = req.params.get('user_id')

        # Validar user_id
        is_valid, error_msg = validate_user_id(user_id)
        if not is_valid:
            return func.HttpResponse(
                json.dumps({'error': error_msg}),
                status_code=400,
                headers=headers
            )

        db = get_db()

        report = db.query(BattleReport)\
            .filter_by(id=report_id, user_id=user_id)\
            .first()

        if not report:
            db.close()
            return func.HttpResponse(
                json.dumps({'error': 'Report not found'}),
                status_code=404,
                headers=headers
            )

        db.delete(report)
        db.commit()
        db.close()

        return func.HttpResponse(
            json.dumps({'message': 'Report deleted successfully'}),
            status_code=200,
            headers=headers
        )

    except Exception as e:
        logging.error(f'Error in DeleteReport: {str(e)}')
        import traceback
        logging.error(traceback.format_exc())

        return func.HttpResponse(
            json.dumps({'error': f'Internal server error: {str(e)}'}),
            status_code=500,
            headers=headers
        )