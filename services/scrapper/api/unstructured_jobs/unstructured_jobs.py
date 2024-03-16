from flask import current_app as app
from ..app import db_name

# Connect to MongoDB
database = app.mongo[db_name]

unstructured_jobs_schema = {
    'title': {'type': 'string', 'required': True},
    'company': {'type': 'string', 'required': True},
    'jobLocation': {'type': 'string', 'required': True},
    'type': {'type': 'string', 'enum': ['Full Time', 'Part Time', 'Contract', 'Internship', 'Temporary', 'Volunteer', 'Other']},
    'skills': {'type': 'array', 'items': 'string'},
    'url': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
    'publishedAt': {'type': 'string'},
    'scrappedAt': {'type': 'date', 'required': True},
    'jobPlace': {'type': 'string', 'enum': ['Remote', 'On Site', 'Hybrid']},
    'numberOfApplicants': {'type': 'int'},
    'neededExperience': {'type': 'int'},
    'education': {'type': 'string'},
    'deletedAt': {'type': 'date', 'default': None}
}

# Create the 'unstructured_jobs' collection and add validation rules
database.create_collection('unstructuredjobs', validator=unstructured_jobs_schema)

# Must create unique index in this collection in mongodb on title, company, date
