from flask import request, jsonify, current_app as app
import simplejson as json

"""from .profile.profile_service import (
    create_profile,
    get_all_profiles
)"""
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
    
def health_check():
    logger.debug("Health check")
    return "Hello World From CV Extractor Service!"

def get_cv_info(data):
    logger.debug("Get CV Info for data: %s", data)
    response = {
        "data": "Beshoy"
    }
    return json.dumps(response)