from flask import request, jsonify, current_app as app
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
from model import model
import json
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Custom Job Service!"

def create_custom_job(data):
    logger.debug("Create custom job")
    prompt = data['jobPrompt']
    job:dict = model.getStructuredJobDetails(prompt)
    # TODO: validation required for the job attributes and values
    return make_response_json(json.dumps(job))