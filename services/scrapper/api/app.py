from flask import (
    Flask,
)
from instance import config
from .logger import logger
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
import os, threading

app = Flask(__name__)

app.config.from_object(config)

# connect to MongoDB
# to use this db, use app.mongo[db]
#db_name = os.getenv('ScrappedJobsDB')

#app.mongo = MongoClient(app.config['MONGODB_URI'])
# Structured Jobs DB
# connect to PostgreSQL database
#db = SQLAlchemy(app)

""" TODO:
    Define cronjob/s starting every X hours to handle this functionalities:
        - Scrape new jobs from jobs websites (initially LinkedIn).
        - Insert only new jobs into unstructured jobs DB.
        - Cronjob every X to scrape active jobs in structured jobs db, that have isScrapped = true, to check whether it is still open or not.
"""

# endpoints for testing
from .index import (
    health_check,
)

# for testing, replica of healthCheck pattern
app.route("/healthCheck", methods=["GET"])(health_check)

# srapped_websites endpoints (for testing)
from .scrapped_websites.linkedin import (
    linkedin_scrape,
)

app.route("/linkedinScrape", methods=["GET"])(linkedin_scrape)
