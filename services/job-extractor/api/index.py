import simplejson as json
from .logger import logger
from .job_extractor.job_extractor import prepare_job

def health_check():
    logger.debug("Health check")
    return "Hello World From Job Extractor Service!"

def get_job_info(data):
    jobs = data.get("jobs")
    
    new_jobs = []
    for job in jobs:
        new_job = prepare_job(job)
        if new_job:
            new_jobs.append(new_job)
    
    return json.dumps({"jobs": new_jobs})