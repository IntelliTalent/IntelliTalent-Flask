import simplejson as json
import requests, os, random, string
from datetime import datetime
from .extract_info.extract_info import extract_info
from .logger import logger
    
def health_check():
    logger.debug("Health check")
    return "Hello World From CV Extractor Service!"

def get_cv_info(data):
    """
    Get CV info
    
    Args:
        data (dict): The data containing the cv link
        
    Returns:
        str: The extracted info from the cv
    """
    logger.debug("Get CV Info for data: %s", data)
    
    # Download the cv from the server and save it to a file
    response = requests.get(data['cvLink'])
    
    # Generate random string of length 8 to handle multiple requests at the same time
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    
    filename = f'cv-{datetime.now().strftime("%d-%m-%Y,%H-%M-%S")}-{random_string}.pdf'
    
    with open(filename, "wb") as f:
        f.write(response.content)

    # Extract the info from the cv
    info_extracted = extract_info(filename)
    
    # Remove the cv file
    os.remove(filename)
    
    response = {
        "info": info_extracted
    }
    return json.dumps(response)