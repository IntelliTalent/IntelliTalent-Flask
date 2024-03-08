from flask import (
    Flask,
)
from .shared.rabbitmq import (
    listen_to_queue,
)
from instance import config
from .logger import logger
import os, threading

def handle_command(command):
    """ TODO:
        Define command/s to handle this functionalities:
           - Should handle an event to extract structured job details and its context (important for Quiz service) from a prompt and return it back. 
           - The user then will see the structured job and edit it, including custom filters, enable quiz generation, and interview quetions, in case of interview, the user will enter a list of questions, then this service will call Jobs service to insert the structured job into DB. 
    """
    
    if command == "healthCheck":
        return health_check()
    
    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_CUSTOM_JOB_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

from .index import (
    health_check,
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)
