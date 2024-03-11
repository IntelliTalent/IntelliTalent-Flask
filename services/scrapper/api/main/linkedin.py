import requests
from bs4 import BeautifulSoup
import time as tm
from urllib.parse import quote
from itertools import groupby
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from datetime import datetime, timedelta, time
import pandas as pd

from ..logger import logger
from instance import config

def get_with_retry(url, retries=config.RETRIES, delay=config.DELAY):
	# Get the URL with retries and delay
	for _ in range(retries):
		try:
			r = requests.get(url, timeout=5)
			return BeautifulSoup(r.content, "html.parser")
		except requests.exceptions.Timeout:
			logger.debug(f"Timeout occurred for URL: {url}, retrying in {delay}s...")
			tm.sleep(delay)
		except Exception as e:
			logger.error(f"An error occurred while retrieving the URL: {url}")
			logger.exception(e)
	return None

def get_job_cards_main_info(soup):
	# Parsing the job card info (title, company, location, date, job_url) from the beautiful soup object
	joblist = []

	try:
		divs = soup.find_all("div", class_="base-search-card__info")
	except:
		logger.error("Empty page, no jobs found")
		return joblist

	for item in divs:
		title = item.find("h3").text.strip()
		
		company = item.find("a", class_="hidden-nested-link")
		
		location = item.find("span", class_="job-search-card__location")
		
		# Get the job posting id
		parent_div = item.parent
		entity_urn = parent_div["data-entity-urn"]
		job_posting_id = entity_urn.split(":")[-1]
		
		# Construct job url
		job_url = f"https://www.linkedin.com/jobs/view/{job_posting_id}/"

		# TODO: Add date
		date_tag_new = item.find("time", class_ = "job-search-card__listdate--new")
		date_tag = item.find("time", class_="job-search-card__listdate")
		date = date_tag["datetime"] if date_tag else date_tag_new["datetime"] if date_tag_new else ""
		logger.debug(date)
		
		# job_description = ""
		job = {
			"title": title,
			"company": company.text.strip().replace("\n", " ") if company else "",
			"location": location.text.strip() if location else "",
			"date": date,
			"job_url": job_url,
			# "job_description": job_description,
			# "applied": 0,
			# "hidden": 0,
			# "interview": 0,
			# "rejected": 0
		}
		joblist.append(job)
	return joblist

def get_job_info(soup):
    # TODO: check what else can we get from the page
    div = soup.find('div', class_='description__text description__text--rich')
    if div:
        # Remove unwanted elements
        for element in div.find_all(['span', 'a']):
            element.decompose()

        # Replace bullet points
        for ul in div.find_all('ul'):
            for li in ul.find_all('li'):
                li.insert(0, '-')

        text = div.get_text(separator='\n').strip()
        text = text.replace('\n\n', '')
        text = text.replace('::marker', '-')
        text = text.replace('-\n', '- ')
        text = text.replace('Show less', '').replace('Show more', '')
        return text
    else:
        return "Could not find Job Description"

def get_search_queries():
	titles = config.JOB_TITLES
	locations = config.JOB_LOCATION
	types = config.JOB_TYPE

	search_queries = []

	for title in titles:
		for location in locations:
			for type in types:
				search_queries.append({
					'keywords': title,
					'location': location,
					'f_WT': type
				})
	return search_queries

def remove_duplicates(joblist):
    # Remove duplicate jobs in the joblist.
    # Duplicate is defined as having the same title and company.
    joblist.sort(key=lambda x: (x['title'], x['company']))
    joblist = [next(g) for k, g in groupby(joblist, key=lambda x: (x['title'], x['company']))]
    return joblist

def safe_detect(text):
    try:
        return detect(text)
    except LangDetectException:
        return 'en'

def get_job_cards(search_queries, rounds = config.ROUNDS, pages_to_scrape = config.PAGES_TO_SCRAPE):
    # Function to get the job cards from the search results page
    all_jobs = []
    
    for _ in range(0, rounds):
        for query in search_queries:
            keywords = quote(query['keywords']) # URL encode the keywords
            location = quote(query['location']) # URL encode the location
            type = query['f_WT']
            timespan = 'r84600' # 60 * 60 * 24 = 24 hours
            
            for i in range (0, pages_to_scrape):
				# Construct the URL
                url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&f_TPR=&f_WT={type}&geoId=&f_TPR={timespan}&start={25*i}"

                soup = get_with_retry(url)
                jobs = get_job_cards_main_info(soup)
                all_jobs = all_jobs + jobs
                
                logger.debug("Finished scraping page: ", url)
	
    logger.debug("Total job cards scraped: ", len(all_jobs))

    all_jobs = remove_duplicates(all_jobs)
    logger.debug("Total job cards after removing duplicates: ", len(all_jobs))
    
    return all_jobs

def convert_date_format(date_string):
    """
    Converts a date string to a date object. 
    
    Args:
        date_string (str): The date in string format.

    Returns:
        date: The converted date object, or None if conversion failed.
    """
    date_format = "%Y-%m-%d"
    try:
        job_date = datetime.strptime(date_string, date_format).date()
        return job_date
    except ValueError:
        logger.error(f"Error: The date for job {date_string} - is not in the correct format.")
        return None

def main():
    start_time = tm.perf_counter()
    job_list = []

    search_queries = get_search_queries()
    all_jobs = get_job_cards(search_queries)

    # Filtering out jobs that are already in the database
    # TODO: Check the the jobs was not scraped before
    logger.info("Total new jobs found after comparing to the database: ", len(all_jobs))

    if len(all_jobs) > 0:
        for job in all_jobs:
            # Get the date in the correct format
            job_date = convert_date_format(job['date'])
            job_date = datetime.combine(job_date, time())
            
            # If job is older than a DAYS_TO_SCRAPE, skip it
            if job_date < datetime.now() - timedelta(days=config.DAYS_TO_SCRAPE):
                continue
            
            logger.debug(f'Found new job: {job['title']}, at {job['company']}, url: {job['job_url']}')
            
            # Get the job description
            desc_soup = get_with_retry(job['job_url'])
            job['job_description'] = get_job_info(desc_soup)
            
            job_list.append(job)
		

		# TODO: Remove this
        df = pd.DataFrame(job_list)
        df['date_loaded'] = datetime.now()
        df['date_loaded'] = df['date_loaded'].astype(str)
        
        df.to_csv('linkedin_jobs.csv', index=False, encoding='utf-8')
    else:
        logger.debug("No jobs found")
    
    end_time = tm.perf_counter()
    logger.info(f"Scraping finished in {end_time - start_time:.2f} seconds")