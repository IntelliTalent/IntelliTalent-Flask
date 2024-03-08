from flask import (
    Flask,
)
from .shared.rabbitmq import (
    listen_to_queue,
)
from instance import config
from flask_sqlalchemy import SQLAlchemy
from .logger import logger
from .shared.helpers import (
    make_response_json
)
import os, threading, json

def handle_command(command, data):
    """ TODO:
        Define command/s to handle this functionalities:
            - Should handle an event that receives a profile id, gets his record from Profile DB, generate a CV, store it with entered_name-randomstring-profileID, and modify the cv path attribute in profile record. 
            - Should handle an event to return all CVs for the user (from all profiles) or a certain profile CV. 
    """
    
    if command == "healthCheck":
        return health_check()
    
    if command == "generateCV":
        return generate_CV(data)
    
    if command == "getAllCVs":
        return get_all_CVs(data)

    if command == "getProfileCV":
        return get_profile_CV(data)
    
    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_CV_GENERATOR_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# connect to PostgreSQL database
db = SQLAlchemy(app)

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

from .index import (
    health_check,
    generate_CV,
    get_all_CVs,
    get_profile_CV
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns


def generate_CV_endpoint(profile_id):
    data = {
        "profile_id": profile_id
    }
    return make_response_json(json.loads(generate_CV(data)))

def get_all_CVs_endpoint(user_id):
    data = {
        "user_id": user_id
    }
    return make_response_json(json.loads(get_all_CVs(data)))

def get_profile_CV_endpoint(profile_id):
    data = {
        "profile_id": profile_id
    }
    return make_response_json(json.loads(get_profile_CV(data)))

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

# for testing, replica of generateCV pattern
app.route("/generateCV/<profile_id>", methods=["POST"])(generate_CV_endpoint)

# for testing, replica of getAllCVs pattern
app.route("/getAllCVs/<user_id>", methods=["GET"])(get_all_CVs_endpoint)

# for testing, replica of getProfileCV pattern
app.route("/getProfileCV/<profile_id>", methods=["GET"])(get_profile_CV_endpoint)
