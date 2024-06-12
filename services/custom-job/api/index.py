from flask import request, current_app as app
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
    job = model.getStructuredJobDetails(prompt)
    return json.dumps(
        {
            'job': job,
            'Content-Type': 'application/json; charset=utf-8',  # Fixed dictionary entry
            'status_code': 200
        }
    )
