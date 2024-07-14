import simplejson as json
from .logger import logger
from .job_extractor.job_extractor import prepare_job

def health_check():
    logger.debug("Health check")
    return "Hello World From Job Extractor Service!"

def get_job_info(data):
    logger.debug("received data")
    logger.debug(data)
    
    jobs = data.get("jobs")
    
    index = 1
    
    new_jobs = []
    for job in jobs:
        try:
            new_job = prepare_job(job)
            if new_job:
                new_jobs.append(new_job)
                
                logger.debug("new job")
                logger.debug(index)
                logger.debug(new_job)
                
                index = index + 1
        except Exception as e:
            logger.exception(e)
            continue
    
    return json.dumps({"jobs": new_jobs})