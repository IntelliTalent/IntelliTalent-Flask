from flask import current_app as app
from ..app import db_name
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
database = app.mongo[db_name]

unstructured_jobs_schema = {
    'title': {'type': 'string', 'required': True},
    'company': {'type': 'string', 'required': True},
    'jobLocation': {'type': 'string', 'required': True},
    'type': {'type': 'string', 'enum': ['Full Time', 'Part Time', 'Contract', 'Internship', 'Temporary', 'Volunteer', 'Other'], 'required': True},
    'skills': {'type': 'array', 'items': 'string'},
    'url': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
    'publishedAt': {'type': 'date'},
    'scrappedAt': {'type': 'date', 'required': True, 'default': datetime.utcnow},
    'jobPlace': {'type': 'string', 'enum': ['Remote', 'On Site', 'Hybrid']},
    'numberOfApplicants': {'type': 'int'},
    'neededExperience': {'type': 'int'},
    'education': {'type': 'string'},
    'deletedAt': {'type': 'date', 'default': None}
}

# Create the 'unstructured_jobs' collection and add validation rules
database.create_collection('unstructuredjobs', validator=unstructured_jobs_schema)
