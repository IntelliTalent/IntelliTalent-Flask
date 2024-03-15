import _thread, requests, json
from ..logger import logger
from instance import config
import time as tm


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
		job = {
			"title": job_data['title'],
			"company": company,
			"jobDescription": job_data['description'] + "\n" + job_data['requirements'] if job_data['requirements'] else job_data['description'],
			"location": job_data['location']['country']['name'],
			"date": job_data['postedAt'],
			"jobUrl": f"https://wuzzuf.net/{job_data['uri']}",
			"jobType": next((job_type for job_type in JOB_TYPE if any(job['displayedName'] == job_type for job in job_data['workTypes'])), "Other"),
			"jobSkills": [skill['name'] for skill in job_data['keywords']],
			"jobPlace": job_data['workplaceArrangement']['displayedName'] if job_data['workplaceArrangement'] else None,
			"neededExperience": job_data['workExperienceYears']['min'],
			"education": job_data['candidatePreferences']['educationLevel']['name'],
		}
		jobs.append(job)
	
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

def wuzzuf_scrape_thread():
    start_time = tm.perf_counter()
    
    search_queries = get_search_queries()
    all_jobs = get_jobs(search_queries)
    
    if len(all_jobs) > 0:
        #TODO: Check for the duplicate jobs
        
        end_time = tm.perf_counter()
        
        logger.info(f"Scraping Wuzzuf finished in {end_time - start_time:.2f} seconds")
        
        # TODO: Save to the db
        with open("api/scrapped_websites/wuzzuf_jobs.json", "w") as f:
            content = {
                "length": len(all_jobs),
                "jobs": all_jobs
            }
            json.dump(content, f, indent=4)
    else:
        logger.debug("No jobs found")


def wuzzuf_scrape():
    _thread.start_new_thread(
            wuzzuf_scrape_thread, ()
        )
    
    return {
        "status": "success",
        "message": "scrapping started"
    }