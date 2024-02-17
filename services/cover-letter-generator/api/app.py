from flask import (
    Flask,
    jsonify,
)
from .index import (
    main,
)
from .logger import (
    logger
)
from .shared.rabbitmq import (
    listen_to_queue,
)
import os, threading

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_COVER_LETTER_QUEUE')

def create_app():
    app = Flask(__name__)
    
    # Start listening to RabbitMQ in a separate thread
    rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
    rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
    rabbitmq_thread.start()

    # doesn't do anything
    app.route("/", methods=["GET"])(main)
    
    # health check, replica of healthCheck pattern
    app.route("/healthCheck", methods=["GET"])(health_check)

    return app 

def handle_command(command):
    if command == "healthCheck":
        return health_check()
    else:
        return {"error": "Unknown command"}
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Cover Letter Service!"
