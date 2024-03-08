from flask import (
    Flask,
)
from .shared.rabbitmq import (
    listen_to_queue,
)
from instance import config
from .logger import logger
from pymongo import MongoClient
import os, threading

def handle_command(command):
    """ TODO:
        Define command/s to handle this functionalities:
           - Once all questions are answered by speech, this service receives an event with the job id, questions, and answers, it should then insert into Interview table records like job_id-user_id-question-answer, the answer is in text (after converting). 
           - Handles an event to display the inteview questions and answers of a certain user (by the recruiter of this job). 
           - If the recruiter of the job decides to pass this user, this service (or this frontend page) should call Filtering service to pass the user from this stage.
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
rabbitmq_queue = os.getenv('RABBITMQ_INTERVIEW_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

# connect to MongoDB
# to use this db, use app.mongo[db]
db_name = os.getenv('InterviewQuestionsDB')

app.mongo = MongoClient(app.config['MONGODB_URI'])

# endpoints for testing
from .index import (
    health_check,
)

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

