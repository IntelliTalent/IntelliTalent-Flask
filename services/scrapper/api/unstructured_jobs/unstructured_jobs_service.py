from datetime import datetime, timezone
from ..logger import logger

def insert_jobs(unstructured_jobs_db, jobs):
    """
    Insert the given jobs into the unstructured jobs collection
    Args:
        unstructured_jobs_db (MongoClient): The unstructured jobs database
        jobs (list): The list of jobs to insert
    Returns:
        None
    """
    try:
        # Get the unstructured jobs collection
        unstructured_jobs_collection = unstructured_jobs_db["unstructuredjobs"]
        
        job = {
            "title": "Software Engineer",
            "company": "Google",
            "jobLocation": "Cairo",
            "type": "Full Time",
            "skills": ["Python", "Java", "C++", "JavaScript"],
            "url": "https://www.google.com",
            "description": "A software engineer is responsible for developing and maintaining software systems.",
            "publishedAt": "2021-07-20T12:00:00Z",
            "scrappedAt": "2021-07-20T12:00:00Z",
            "jobPlace": "Remote",
            "numberOfApplicants": 10,
            "neededExperience": 2,
            "education": "Bachelor's degree",
            "deletedAt": None
        }
        
        jobs.append(job)
        
        current_time = datetime.now(timezone.utc)
        
        # Add the scrappedAt field to the jobs
        for job in jobs:
            job["scrappedAt"] = current_time
        
        # Insert the jobs into the collection
        unstructured_jobs_collection.insert_many(jobs, ordered=False)
    except Exception as e:
        # Ignored because it is probably a common error of duplicated compound key of title, company, publishedAt
        pass