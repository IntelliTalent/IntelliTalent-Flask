from flask import request, jsonify, current_app as app
import simplejson as json

from .shared.helpers import (
    make_response_json,
)
from .logger import logger
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Job Extractor Service!"

def get_job_info(data):
    logger.debug("Get Job Info for data: %s", data)
    response = {
        "data": "Beshoy"
    }
    return json.dumps(response)