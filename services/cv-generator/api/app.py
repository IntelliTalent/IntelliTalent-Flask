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
            - Should handle an event generates a CV given user profile. 
    """
    
    if command == "healthCheck":
        return health_check()
    
    if command == "generateCV":
        return generate_CV(data)
    
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

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

from .index import (
    health_check,
    generate_CV,
    get_file
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns


def generate_CV_endpoint():
    data = {
        "fullname": "Moaz Mohamed"
    }
    return make_response_json(json.loads(generate_CV(data)))

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

# for testing, replica of generateCV pattern
app.route("/generateCV", methods=["POST"])(generate_CV_endpoint)

# route files
app.route("/generated-cvs/<filename>", methods=["GET"])(get_file)
