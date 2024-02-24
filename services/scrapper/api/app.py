from flask import (
    Flask,
)
from instance import config
from .logger import logger
from pymongo import MongoClient
import os, threading

app = Flask(__name__)

app.config.from_object(config)

# connect to MongoDB
# to use this db, use app.mongo[db]
db_name = os.getenv('ScrappedJobsDB')

app.mongo = MongoClient(app.config['MONGODB_URI'])

""" TODO:
    Define cronjob/s starting every X hours to handle this functionalities:
        - Scrape new jobs from jobs websites (initially LinkedIn).
        - Insert only new jobs into unstructured jobs DB.
"""

# endpoints for testing
from .index import (
    health_check,
)

# health check endpoint
app.route("/healthCheck", methods=["GET"])(health_check)

