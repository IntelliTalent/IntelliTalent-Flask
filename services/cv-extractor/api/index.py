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
    host = os.getenv('SERVER_HOST')
    response = requests.get(f"http://{host}:3000/api/v1/cv/{data['fileId']}")
    with open("cv.pdf", "wb") as f:
        f.write(response.content)
    
    
    info_extracted = extract_info()
    
    os.remove("cv.pdf")
    
    response = {
        "info": info_extracted
    }
    return json.dumps(response)