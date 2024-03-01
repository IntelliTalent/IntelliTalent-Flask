from flask import (
    Flask,
)
from .shared.rabbitmq import (
    listen_to_queue,
)
from instance import config
from flask_sqlalchemy import SQLAlchemy
from .logger import logger
import os, threading

def handle_command(command):
    """ TODO:
        Define command/s to handle this functionalities:
            - Should handle an event that receives a profile id, gets his record from Profile DB, generate a CV, store it with entered_name-randomstring-profileID, and modify the cv path attribute in profile record. 
            - Should handle an event to return all CVs for the user (from all profiles) or a certain profile CV. 
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
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns

# health check, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

