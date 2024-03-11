from flask import request, jsonify, current_app as app
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
import json
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Custom Job Service!"

def create_custom_job():
    job = {
        'title': 'Software Engineer',
        'company': 'Google',
        'jobLocation': 'Remote',
        'type': 'Full-time',
        'skills': ['Python', 'Django', 'React'],
        'jobPlace': 'Remote',
        'neededExperience': '3 years',
        'education': 'Bachelor',
        'csRequired': True,
    }
    return json.dumps(job)