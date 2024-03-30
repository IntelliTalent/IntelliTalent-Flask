from flask import request, jsonify, current_app as app
import simplejson as json

from .shared.helpers import (
    make_response_json,
)
from .logger import logger
from .job_extractor.job_extractor import prepare_job

def health_check():
    logger.debug("Health check")
    return "Hello World From Job Extractor Service!"

def get_job_info(data):
    jobs = data.get("jobs")
    
    new_jobs = []
    for job in jobs:
        new_jobs.append(prepare_job(job))
    
    return json.dumps({"jobs": new_jobs})