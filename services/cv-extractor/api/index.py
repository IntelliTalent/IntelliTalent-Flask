from flask import request, jsonify, current_app as app
import simplejson as json
import requests, os
from .extract_info.extract_info import extract_info

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
    
    # Download the cv from the server and save it to a file
    response = requests.get(data['cvLink'])
    with open("cv.pdf", "wb") as f:
        f.write(response.content)

    # Extract the info from the cv
    info_extracted = extract_info()
    
    # Remove the cv file
    os.remove("cv.pdf")
    
    response = {
        "info": info_extracted
    }
    return json.dumps(response)