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

def handle_command(command, data):
    """ TODO:
        Define command/s to handle this functionalities:
           - Should handle an event to generate a new quiz related to job skills, save it in the database with a record like job_id-user_id-questions-random_slug-score, and return a link (with the slug in it like https://intellitalent.io/jobs/hf45s4adg7) to the page that will display this record.
           - At the submission of quiz answers, the service should calculate the success score and call the Filteration service with this data.
    """

    if command == "healthCheck":
        return health_check()

    # data should be x of skills and number of required context
    if command == "generateQuiz":
        return get_questions_for_skills(data.get("skills"), data.get("num_of_contexts") ,data.get("number_of_questions", 20))
    if command == "generateNumberOfQuizzes":
        return generateNumberOfQuizzes(data.get("skills"), data.get("num_of_contexts"), data.get("number_of_questions_per_context"), data.get("number_of_quizzes", 1))

    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_QUIZ_GENERATOR_QUEUE')

print(f"RabbitMQ: {rabbitmq_user}@{rabbitmq_host}:{rabbitmq_port} - {rabbitmq_queue}")

app = Flask(__name__)

app.config.from_object(config)

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

# connect to MongoDB
# to use this db, use app.mongo[db]
db_name = os.getenv('QuizzesDB')

app.mongo = MongoClient(app.config['MONGODB_URI'])

# endpoints for testing
from .index import (
    health_check,
    get_questions_for_skills,
    generateNumberOfQuizzes
)

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

