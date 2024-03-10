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
    return "Hello World From Interview Service!"


def submit_interview():
    response = {
        "status": 200,
        "message": "submitted interview successfully"
    }
    return json.dumps(response)

def get_user_answers():
    response = [
        {
            "question": "Tell me about yourself",
            "answer": "I am a software engineer"
        },
        {
            "question": "What is your experience",
            "answer": "I have 3 years of experience"
        }
    ]
    return json.dumps(response)