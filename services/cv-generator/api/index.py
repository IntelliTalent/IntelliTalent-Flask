from flask import request, jsonify, current_app as app
"""from .profile.profile_service import (
    create_profile,
    get_all_profiles
)"""
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
        "pdf": "https://www.google.com",
        "word": "https://www.google.com"
    }
    return json.dumps(response)

def get_all_CVs(data):
    logger.debug("Getting all CVs for data: %s", data)
    response = {
        "cvs": [
            {
                "pdf": "https://www.google.com",
                "word": "https://www.google.com",
                "profile_id": "1234"
            },
            {
                "pdf": "https://www.google.com",
                "word": "https://www.google.com",
                "profile_id": "1235"
            }
        ]
    }
    return json.dumps(response)

def get_profile_CV(data):
    logger.debug("Getting CV for data: %s", data)
    response = {
        "pdf": "https://www.google.com",
        "word": "https://www.google.com"
    }
    return json.dumps(response)
