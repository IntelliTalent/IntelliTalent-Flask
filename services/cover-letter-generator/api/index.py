import simplejson as json
from flask.helpers import send_file
from instance import config
from .helpers.helper import (
    generate_cover_letter_data,
    preprocess_user_info
)
from .logger import logger

'''def main():
    """
    main function
    """
    try:
        logger.debug("Main function")
        new_profile = create_profile("John Doe")
        
        logger.debug("New profile created = %s", new_profile)

        profiles = get_all_profiles()
        
        formfieldsdb = app.mongo["formfieldsdb"]
        
        dummy_collection = formfieldsdb["dummy_collection"]
        
        # insert a dummy document
        dummy_collection.insert_one({"name": "John Doe"})
        
        # retrieve all documents
        dummy = []
        for doc in dummy_collection.find():
            doc["_id"] = str(doc["_id"])
            dummy.append(doc)
            
        logger.debug("Dummy collection = %s", dummy)
        app.redis_client.set("products", "dsfdsf")
        products = app.redis_client.get("products")
        
        products = products.decode('utf-8')
        
        logger.debug("Products = %s", products)
        
        return {
            "profiles": profiles,
            "dummy": dummy,
            "products": products
        }
    except Exception as e:
        return make_response_json({"message": str(e), "status": 500}, 500)'''
    
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
        
        # access profile data from data["profile"]
        response = {
            "word": f"http://{config.server_ip}:3002/{filename}.docx",
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

def get_file(filename):
    try:
        return send_file(f"generated-coverletters/{filename}")
    except Exception as e:
        logger.exception("Error while getting file: %s", e)
        return json.dumps({
            "message": "Error while getting file!",
            "error": str(e),
            "status": 404
        })
