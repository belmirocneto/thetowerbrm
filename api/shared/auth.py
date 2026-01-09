import os
import logging

API_KEY = os.getenv('API_KEY')

def validate_api_key(req) -> tuple[bool, str]:
    """
    Valida a API key do request
    Returns: (is_valid, error_message)
    """
    api_key = req.headers.get('X-API-Key')

    if not api_key:
        return False, 'API key missing'

    if api_key != API_KEY:
        logging.warning(f'Invalid API key attempt')
        return False, 'Invalid API key'

    return True, ''

def validate_user_id(user_id: str) -> tuple[bool, str]:
    """
    Valida o user_id
    Returns: (is_valid, error_message)
    """
    if not user_id:
        return False, 'user_id is required'

    if len(user_id) != 16:
        return False, 'user_id must be 16 characters'

    return True, ''