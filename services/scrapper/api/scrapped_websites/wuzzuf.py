import requests, json
from ..logger import logger
from instance import config
from ..unstructured_jobs.unstructured_jobs_service import insert_jobs
import time as tm
from datetime import datetime
from bs4 import BeautifulSoup

JOB_QUERY = {
    "startIndex": 0,
    "pageSize": 25,
    "longitude": 0,
    "latitude": 0,
    "query": "",			# Change this to the job title
    "searchFilters": { 
        "post_date": ["within_24_hours"],
        "country": []		# Change this to the location
    }
}

WUZZUF_SEARCH_API = 'https://wuzzuf.net/api/search/job'
WUZZUF_JOB_API = 'https://wuzzuf.net/api/job?filter[other][ids]='
HEADERS = {'content-type': 'application/json;charset=UTF-8'}

JOB_TYPE = [
    "Part Time",
    "Full Time",
    "Contract",
    "Internship",
    "Temporary",
    "Volunteer"
]

def get_search_queries():
    """
    Get the search queries (enumerate the job titles and locations) from the config file

    Args:
        None

    Returns:
        list: The list of search queries
    """
    titles = config.JOB_TITLES
    locations = config.JOB_LOCATIONS

    search_queries = []

    for title in titles:
        for location in locations:
            search_queries.append({
                "title": title,
                "location": location,
            })

    return search_queries

def get_jobs_details(jobs):
    """
    Get the details of the jobs from the jobs array

    Args:
        jobs (list): The list of jobs returned from the WUZZUF API

    Returns:
        list: The list of jobs with details ready to be inserted into the database
    """
    job_ids, job_companies = [], []
    for job in jobs:
        job_ids.append(job['id'])

        # Get the company name
        for fields in job['attributes']['computedFields']:
            if fields['name'] == 'company_name':
                job_companies.append(fields['value'][0])

    # Prepare the request to get the job details
    wuzzuf_job_api = WUZZUF_JOB_API + ','.join(job_ids)
    job_details_json = requests.get(wuzzuf_job_api).json()
    
    jobs = []
    
    for company, job in zip(job_companies, job_details_json['data']):
        job_data = job['attributes']

        # Format datetime object into desired output format
        published_at_datetime = datetime.strptime(job_data['postedAt'], "%m/%d/%Y %H:%M:%S")
        published_at = published_at_datetime.strftime("%Y-%m-%d")
        
        # Format the description to remove HTML tags
        description_html = job_data['description'] + "\n" + job_data['requirements'] if job_data['requirements'] else job_data['description']
        description_soap = BeautifulSoup(description_html, 'html.parser')
        description = description_soap.get_text(separator="\n").strip()
        description = description.replace("\n\n", "")
        description = description.replace("::marker", "-")
        description = description.replace("-\n", "- ")

        job = {
            "jobId": job['id'],
            "title": job_data['title'],
            "company": company,
            "description": description,
            "jobLocation": job_data['location']['country']['name'],
            "publishedAt": published_at,
            "url": f"https://wuzzuf.net/{job_data['uri']}",
            "type": next((job_type for job_type in JOB_TYPE if any(job['displayedName'] == job_type for job in job_data['workTypes'])), "Other"),
            "skills": [skill['name'] for skill in job_data['keywords']],
            "jobPlace": job_data['workplaceArrangement']['displayedName'] if job_data['workplaceArrangement'] else None,
            "neededExperience": job_data['workExperienceYears']['min'],
            "education": job_data['candidatePreferences']['educationLevel']['name'],
        }
        jobs.append(job)
        
        logger.debug(f"(Wuzzuf) Found new job: {job['title']} at {job['company']}, url: {job['url']}")
    
    return jobs

def get_jobs(search_queries, pages_to_scrape=config.PAGES_TO_SCRAPE):
    """
    Get the jobs from the WUZZUF API

    Args:
        search_queries (list): The list of search queries
        pages_to_scrape (int, optional): The number of pages to scrape. Defaults to PAGES_TO_SCRAPE.

    Returns:
        list: The list of jobs
    """
    all_jobs = []

    for query in search_queries:
        title = query["title"]
        location = query["location"]
        
        for i in range (0, pages_to_scrape):
            JOB_QUERY["startIndex"] = i
            JOB_QUERY["query"] = title
            JOB_QUERY["searchFilters"]["country"] = [location]
            data = json.dumps(JOB_QUERY)
            job_search_json = requests.post(WUZZUF_SEARCH_API , headers=HEADERS , data=data).json()

            jobs = get_jobs_details(job_search_json['data'])
            all_jobs += jobs

    return all_jobs

def wuzzuf_scrape_thread(unstructured_jobs_db):
    """
    Scrape jobs from WUZZUF

    Args:
        unstructured_jobs_db (MongoClient): The unstructured jobs database
    Returns:
        None
    """
    start_time = tm.perf_counter()

    search_queries = get_search_queries()
    all_jobs = get_jobs(search_queries)

    jobs_length = len(all_jobs)
    
    if jobs_length > 0:		
        # insert in db, note that there is an index on title, company, and publishedAt fields, that handls duplicated jobs
        insert_jobs(unstructured_jobs_db, all_jobs)
        
        logger.debug(f"(Wuzzuf) Total job cards scraped: {jobs_length}")
    else:
        logger.debug("(Wuzzuf) No jobs found")
    
    end_time = tm.perf_counter()
    logger.info(f"Scraping Wuzzuf finished in {end_time - start_time:.2f} seconds")

def is_expired(date_string):
    """
    Check if the date is expired

    Args:
        date_string (str): The date string

    Returns:
        bool: True if the date is expired, False otherwise
    """
    # Parse the date string into a datetime object
    expiration_date = datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")
    
    # Get the current date and time
    current_date = datetime.now()
    
    # Compare the expiration date with the current date and time
    return expiration_date < current_date

def wuzzuf_check_active_jobs(jobs):
    """
    Check the active jobs
    Args:
        jobs (list): The list of jobs
    Returns:
        dict: A dictionary containing the jobs status
    """
    
    # Get the job ids and prepare the request
    job_ids = [job["jobId"] for job in jobs]
    active_jobs = {}
    
    if len(job_ids):
        # Prepare the request to get the job details
        wuzzuf_job_api = WUZZUF_JOB_API + ','.join(job_ids)
        job_details_json = requests.get(wuzzuf_job_api).json()
        
        # Results map: [job_id] = is_active
        for job in job_details_json["data"]:
            job_data = job["attributes"]
            expire_data = job_data["expireAt"]
            active_jobs[job["id"]] = not is_expired(expire_data)
    
    # Check the active jobs
    for job in jobs:
        job["isActive"] = active_jobs.get(job["jobId"], False)
        del job["url"]
        del job["jobId"]
    
    return jobs
