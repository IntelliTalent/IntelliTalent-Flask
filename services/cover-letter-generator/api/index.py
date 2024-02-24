from flask import request, jsonify, current_app as app
"""from .profile.profile_service import (
    create_profile,
    get_all_profiles
)"""
from .helpers.helper import (
    make_response_json,
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
    logger.debug("Health check")
    return "Hello World From Cover Letter Service!"