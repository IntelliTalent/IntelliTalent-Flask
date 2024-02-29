from flask import current_app as app
from ..app import db_name

# Connect to MongoDB
database = app.mongo[db_name]

interviews_schema = {
    'profileId': {'type': 'string', 'required': True},
    'jobId': {'type': 'string', 'required': True},
    'randomSlug': {'type': 'string', 'required': True},
    'textAnswers': {'type': 'array', 'items': 'string'},
    'recordedAnswers': {'type': 'array', 'items': 'string'},
    'questions': {'type': 'array', 'items': 'string', 'required': True}
}

database.create_collection('interviews', validator=interviews_schema)
