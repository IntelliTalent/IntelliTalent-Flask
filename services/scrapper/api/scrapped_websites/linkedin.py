from ..logger import logger
from instance import config
from ..unstructured_jobs.unstructured_jobs_service import insert_jobs
from bs4 import BeautifulSoup
import requests
import time as tm
from urllib.parse import quote
from itertools import groupby
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Constants

# Number of times to try the same query (linkedin gives different results each time)
ROUNDS = 1

# The number of pages to scrape for each search query
PAGES_TO_SCRAPE = 10

# Number of times to retry to connect to the same url
RETRIES = 4
DELAY = 1

# 1: onsite - 2: remote - 3: hybrid
JOB_PLACES = [1, 2, 3]

JOB_PLACES_MAP = {
    1: "On Site",
    2: "Remote",
    3: "Hybrid",
}

# Max number of days to scrape (take only the last DAYS_TO_SCRAPE days) 
DAYS_TO_SCRAPE = 1

def get_with_retry(url, retries=RETRIES, delay=DELAY):
    """
    Get the URL with retries and delay
    Args:
        url (str): The URL to get
        retries (int): The number of times to retry to connect to the same url
        delay (int): The delay between retries
    Returns:
        BeautifulSoup: The beautiful soup object
    """
    # Get the URL with retries and delay
    for _ in range(retries):
        try:
            r = requests.get(url)
            return BeautifulSoup(r.content, "html.parser")
        except requests.exceptions.Timeout:
            logger.debug(f"Timeout occurred for URL: {url}, retrying in {delay}s...")
            tm.sleep(delay)
        except Exception as e:
            logger.error(f"An error occurred while retrieving the URL: {url}")
            logger.exception(e)
    return None

def get_job_cards_main_info(soup, place):
    """
    Get the job card info from the search results page
    Args:
        soup (BeautifulSoup): The beautiful soup object
        place (str): The place of the job (On Site, Hybrid, Remote)
    Returns:
        list: The list of job cards
    """
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
        job_url = f"http://www.linkedin.com/jobs/view/{job_posting_id}/"

        date_tag_new = item.find("time", class_ = "job-search-card__listdate--new")
        date_tag = item.find("time", class_="job-search-card__listdate")
        date = date_tag["datetime"] if date_tag else date_tag_new["datetime"] if date_tag_new else ""
        
        job = {
            "title": title,
            "company": company.text.strip().replace("\n", " ") if company else "",
            "jobLocation": location.text.strip() if location else "",
            "publishedAt": date,
            "url": job_url,
            "jobPlace": JOB_PLACES_MAP[place],
        }
        joblist.append(job)
    return joblist

def get_job_description(soup):
    """
    Get the job description from the job page
    Args:
        soup (BeautifulSoup): The beautiful soup object
    Returns:
        str: The job description
    """
    div = soup.find("div", class_="description__text description__text--rich")
    if div:
        # Remove unwanted elements
        for element in div.find_all(["span", "a"]):
            element.decompose()

        # Replace bullet points
        for ul in div.find_all("ul"):
            for li in ul.find_all("li"):
                li.insert(0, "-")

        text = div.get_text(separator="\n").strip()
        text = text.replace("\n\n", "")
        text = text.replace("::marker", "-")
        text = text.replace("-\n", "- ")
        text = text.replace("Show less", "").replace("Show more", "")
        return text
    else:
        logger.error("(LinkedIn) Could not find Job Description, retrying...")
        return "Could not find Job Description"

def get_search_queries():
    """
    Get the search queries to use
    Args:
        None
    Returns:
        list: The list of search queries
    """
    titles = config.JOB_TITLES
    locations = config.JOB_LOCATIONS
    places = JOB_PLACES

    search_queries = []

    for title in titles:
        for location in locations:
            for place in places:
                search_queries.append({
                    "keywords": title,
                    "location": location,
                    "place": place
                })
                
    return search_queries

def remove_duplicates(joblist):
    """
    Remove duplicate jobs in the joblist
    Args:
        joblist (list): The list of jobs
    Returns:
        list: The list of jobs with duplicates removed
    """
    # Remove duplicate jobs in the joblist.
    # Duplicate is defined as having the same title and company.
    joblist.sort(key=lambda x: (x["title"], x["company"]))
    joblist = [next(g) for k, g in groupby(joblist, key=lambda x: (x["title"], x["company"]))]
    return joblist

def safe_detect(text):
    """
    Detect the language of the given text
    Args:
        text (str): The text to detect its language
    Returns:
        str: The detected language
    """
    try:
        return detect(text)
    except LangDetectException:
        return "en"

def get_job_cards(search_queries, rounds = ROUNDS, pages_to_scrape = PAGES_TO_SCRAPE):
    """
    Get the job cards from the search results page
    Args:
        search_queries (list): The list of search queries to use
        rounds (int): The number of times to try the same query
        pages_to_scrape (int): The
    Returns:
        list: The list of job cards
    """
    # Function to get the job cards from the search results page
    all_jobs = []
    
    for _ in range(0, rounds):
        for query in search_queries:
            keywords = quote(query["keywords"]) # URL encode the keywords
            location = quote(query["location"]) # URL encode the location
            place = query["place"]
            timespan = "r" + str(DAYS_TO_SCRAPE * 24 * 60 * 60)
            
            for i in range (0, pages_to_scrape):
				# Construct the URL
                url = f"http://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&f_WT={place}&f_TPR={timespan}&start={25*i}"

                soup = get_with_retry(url)
                jobs = get_job_cards_main_info(soup, place)
                
                if len(jobs) == 0:
                    logger.debug("(LinkedIn) No jobs found on page: %s", url)
                    break
                
                all_jobs = all_jobs + jobs
                
                logger.debug("(LinkedIn) Finished scraping page: %s", url)
	
    logger.debug("(LinkedIn) Total job cards scraped: %s", len(all_jobs))

    all_jobs = remove_duplicates(all_jobs)
    logger.debug("(LinkedIn) Total job cards after removing duplicates: %s", len(all_jobs))
    
    return all_jobs

def linkedin_scrape_thread(unstructured_jobs_db):
    """
    The main linkedin scraping function
    Args:
        unstructured_jobs_db (MongoClient): The unstructured jobs database
    Returns:
        None
    """
    start_time = tm.perf_counter()
    job_list = []

    search_queries = get_search_queries()
    all_jobs = get_job_cards(search_queries)

    if len(all_jobs) > 0:
        for job in all_jobs:
            logger.debug(f"(LinkedIn) Found new job: {job['title']}, at {job['company']}, url: {job['url']}")
            
            for _ in range(RETRIES):
                # Get the job description
                desc_soup = get_with_retry(job["url"])
                
                job["description"] = get_job_description(desc_soup)
                
                if job["description"] != "Could not find Job Description":
                    break
            
            job_list.append(job)
            
        # insert in db, note that there is an index on title, company, and publishedAt fields, that handls duplicated jobs
        insert_jobs(unstructured_jobs_db, job_list)
    else:
        logger.debug("(LinkedIn) No jobs found")
    
    end_time = tm.perf_counter()
    logger.info(f"Scraping LinkedIn finished in {end_time - start_time:.2f} seconds")
