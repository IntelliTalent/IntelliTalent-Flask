from flask import request, jsonify, current_app as app
from .profile.profile_service import (
    create_profile,
    get_all_profiles
)
from .helpers.helper import (
    make_response_json,
)
from .logger import logger

def main():
    """
    main function
    """
    try:
        logger.debug("Main function")
        new_profile = create_profile("John Doe")
        
        logger.debug("New profile created = %s", new_profile)

        profiles = get_all_profiles()
        
        
        return jsonify(profiles)
    except Exception as e:
        return make_response_json({"message": str(e), "status": 500}, 500)
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Cover Letter Service!"