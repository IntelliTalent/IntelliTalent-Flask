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
#app.mongo = MongoClient(app.config['MONGODB_URI'])

"""from .index import (
    main,
)"""

# endpoints for testing
from .index import (
    health_check,
)

# health check endpoint
app.route("/healthCheck", methods=["GET"])(health_check)

