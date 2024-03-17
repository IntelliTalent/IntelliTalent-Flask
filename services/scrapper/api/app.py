from flask import (
    Flask,
)
from instance import config
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import atexit, os

app = Flask(__name__)

app.config.from_object(config)

# connect to MongoDB
# to use this db, use app.mongo[db]
db_name = os.getenv('ScrappedJobsDB')

app.mongo = MongoClient(app.config['MONGODB_URI'])
# Structured Jobs DB
# connect to PostgreSQL database
db = SQLAlchemy(app)

""" TODO:
    Define cronjob/s starting every X hours to handle this functionalities:
        - Scrape new jobs from jobs websites (initially LinkedIn).
        - Insert only new jobs into unstructured jobs DB.
        - Cronjob every X to scrape active jobs in structured jobs db, that have isScrapped = true, to check whether it is still open or not.
"""

# endpoints for testing
from .index import (
    health_check,
    scrape,
)

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

# srape endpoint (for testing)

app.route("/scrape", methods=["GET"])(scrape)

scheduler = BackgroundScheduler(timezone=utc)

# Cronjob to start the scraping process every 3 hours, passing the unstructured jobs db connection
scheduler.add_job(func=scrape, args=(app.mongo[db_name],), trigger="interval", hours=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
