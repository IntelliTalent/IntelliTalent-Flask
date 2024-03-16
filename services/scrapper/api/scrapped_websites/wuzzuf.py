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
    job_ids, job_companies = [], []
    for job in jobs:
        job_ids.append(job['id'])

        for fields in job['attributes']['computedFields']:
            if fields['name'] == 'company_name':
                job_companies.append(fields['value'][0])

    wuzzuf_job_api = WUZZUF_JOB_API + ','.join(job_ids)
    job_details_json = requests.get(wuzzuf_job_api).json()
    
    jobs = []
    
    for company, job in zip(job_companies, job_details_json['data']):
        job_data = job['attributes']

        published_at = job_data['postedAt']
  
        # Parse input string into a datetime object
        published_at_datetime = datetime.strptime(published_at, "%m/%d/%Y %H:%M:%S")

        # Format datetime object into desired output format
        published_at = published_at_datetime.strftime("%Y-%m-%d")
  
        description_html = job_data['description'] + "\n" + job_data['requirements'] if job_data['requirements'] else job_data['description']
  
        description_soap = BeautifulSoup(description_html, 'html.parser')
  
        description = description_soap.get_text(separator="\n").strip()
        description = description.replace("\n\n", "")
        description = description.replace("::marker", "-")
        description = description.replace("-\n", "- ")

        job = {
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

def get_jobs(search_queries):
    all_jobs = []

    for query in search_queries:
        title = query["title"]
        location = query["location"]
        
        JOB_QUERY["query"] = title
        JOB_QUERY["searchFilters"]["country"] = [location]
        data = json.dumps(JOB_QUERY)
        job_search_json = requests.post(WUZZUF_SEARCH_API , headers=HEADERS , data=data).json()

        jobs = get_jobs_details(job_search_json['data'])
        all_jobs += jobs

    return all_jobs

def wuzzuf_scrape_thread(unstructured_jobs_db):
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
        