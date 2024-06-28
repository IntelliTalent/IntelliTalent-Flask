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
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import atexit, os, threading, json

def handle_command(command, data):
    if command == "healthCheck":
        return health_check()
    
    if command == "checkActiveJobs":
        return check_active_jobs(data)
    else:
        return {"error": "Unknown command"}

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT') 
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_SCRAPPER_QUEUE')

app = Flask(__name__)

app.config.from_object(config)

# connect to MongoDB
# to use this db, use app.mongo[db]
db_name = os.getenv('ScrappedJobsDB')

app.mongo = MongoClient(app.config['MONGODB_URI'])

app.rabbitmq_user = rabbitmq_user
app.rabbitmq_pass = rabbitmq_pass
app.rabbitmq_host = rabbitmq_host
app.rabbitmq_port = rabbitmq_port
app.rabbitmq_queue = rabbitmq_queue
app.jobs_queue = os.getenv('RABBITMQ_JOB_QUEUE')

# Start listening to RabbitMQ in a separate thread
rabbitmq_thread = threading.Thread(target=listen_to_queue, args=(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_queue, handle_command))
rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
rabbitmq_thread.start()

# endpoints for testing
from .index import (
    health_check,
    scrape,
    check_active_jobs,
)

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

# scrape endpoint (for testing)
def scrape_endpoint():
    return make_response_json(scrape(app.mongo[db_name]))

app.route("/scrape", methods=["GET"])(scrape_endpoint)

# check active endpoint (for testing)

def check_active_jobs_endpoint():
    body = request.get_json()

    return make_response_json(json.loads(check_active_jobs(body)))

app.route("/checkActiveJobs", methods=["POST"])(check_active_jobs_endpoint)

scheduler = BackgroundScheduler(timezone=utc)

# Cronjob to start the scraping process every 3 hours, passing the unstructured jobs db connection

# TODO: uncomment this when production ready
#scheduler.add_job(func=scrape, args=(app.mongo[db_name],), trigger="interval", hours=3)
#scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
