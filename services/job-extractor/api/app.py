from flask import (
    Flask,
    request
)
from .shared.rabbitmq import (
    listen_to_queue,
)
from .shared.helpers import (
    make_response_json
)
from instance import config
from .logger import logger
import os, threading, json

def handle_command(command, data):
    if command == "healthCheck":
        return health_check()
    
    if command == "extractInfo":
        return get_job_info(data)
    
    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_JOB_EXTRACTOR_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

from .index import (
    health_check,
    get_job_info
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

def convert_unstructured_jobs_endpoint():
    body = request.get_json()

    return make_response_json(get_job_info(body))

app.route("/convert", methods=["POST"])(convert_unstructured_jobs_endpoint)