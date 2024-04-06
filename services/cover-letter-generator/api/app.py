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
from flask_sqlalchemy import SQLAlchemy
from .logger import logger
"""from pymongo import MongoClient
import redis"""
import os, threading, json

def handle_command(command, data):
    if command == "healthCheck":
        return health_check()
    
    if command == "generateCoverLetter":
        return generate_cover_letter(data)
    
    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_COVER_LETTER_GENERATOR_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# connect to PostgreSQL database
db = SQLAlchemy(app)

# (just for testing)
# connect to MongoDB
#app.mongo = MongoClient(app.config['MONGODB_URI'])

# (just for testing)
# connect to redis
# initialize redis
"""logger.debug("Redis host: %s", os.getenv("REDIS_HOST"))
logger.debug("Redis port: %s", os.getenv("REDIS_PORT"))
logger.debug("Redis pass: %s", os.getenv("REDIS_PASSWORD"))
try:
    pool = redis.ConnectionPool(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        db=0,
        password=os.getenv("REDIS_PASSWORD"),
        socket_timeout=10,
        retry_on_timeout=True,
    )
    redis_client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
    app.redis_client = redis_client
except Exception as e:
    logger.exception(e)"""

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

from .index import (
    health_check,
    generate_cover_letter,
    get_file
)

# endpoints for testing, the actual endpoints communicate through RabbitMQ patterns

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

def generate_cover_letter_endpoint():
    body = request.get_json()
    return make_response_json(json.loads(generate_cover_letter(body)))

# for testing, replica of generateCoverLetter pattern
app.route("/generateCoverLetter", methods=["POST"])(generate_cover_letter_endpoint)

# route files
app.route("/generated/<filename>", methods=["GET"])(get_file)
