import simplejson as json
from .helpers.helper import (
    generate_cover_letter_data,
    preprocess_user_info,
    upload_file,
)
from .logger import logger
    
def health_check():
    """
    Health check
    """
    logger.debug("Health check")
    return "Hello World From Cover Letter Generator Service!"

def generate_cover_letter(data):
    """
    Generate Cover Letter

    Args:
        data (dict): data to generate cover letter
    Returns:
        str: response
    """
    try:
        logger.debug("Generating Cover Letter for data: %s", data)
        
        user_info = data["profile"]
        
        wanted_job_info = {
            "jobTitle": data["jobTitle"],
            "companyName": data["companyName"]
        }
        
        preprocess_user_info(user_info)
        
        logger.debug("User Info: %s", user_info)
        
        cover_letter_text, filename = generate_cover_letter_data(user_info, wanted_job_info)
        
        word_link = upload_file(filename)
        
        response = {
            "word": word_link,
            "text": cover_letter_text
        }
        return json.dumps(response)
    except Exception as e:
        logger.exception("Error while generating cover letter: %s", e)
        return json.dumps({
            "message": "Error while generating cover letter!",
            "error": str(e),
            "status": 500
        })
