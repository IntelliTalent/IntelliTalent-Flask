from flask import (
    Flask,
)
from instance import config
from .logger import logger
from pymongo import MongoClient
import os, threading

def health_check():
    return "Hello World From Cover Letter Service!"

app = Flask(__name__)

app.config.from_object(config)

# connect to MongoDB
#app.mongo = MongoClient(app.config['MONGODB_URI'])

"""from .index import (
    main,
)"""

# endpoints for testing

# health check endpoint
app.route("/healthCheck", methods=["GET"])(health_check)

