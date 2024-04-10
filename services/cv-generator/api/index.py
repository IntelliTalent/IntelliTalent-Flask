from flask import request, jsonify, current_app as app
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
import json
    
def health_check():
    logger.debug("Health check")
    return "Hello World From CV Generator Service!"

def generate_CV(data):
    logger.debug("Generating CV for data: %s", data)
    response = {
        "word": "https://www.google.com"
    }
    return json.dumps(response)
