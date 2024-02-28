from flask import request, jsonify, current_app as app
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Custom Job Service!"