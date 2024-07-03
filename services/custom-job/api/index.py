from .logger import logger
import json

from helpers.helper import extract_job_titles, extract_skills, extract_locations, extract_job_types, extract_years_of_experience, extract_job_end_dates, extract_company_names, extract_countries_cities, extract_languages
    
def health_check():
    logger.debug("Health check")
    return "Hello World From Custom Job Service!"


def create_custom_job(data):
    """
    return structured job details based on the job prompt using NLP techniques

    Args:
        data (string): prompt for the job
    Returns:
        serialized json : structured job details
    """
    logger.debug("Create custom job")
    prompt = data['jobPrompt']

    countries, cities = extract_countries_cities(prompt)

    job = {
        "title": extract_job_titles(prompt),
        "skills": extract_skills(prompt),
        "jobLocation": extract_locations(prompt),
        "type": extract_job_types(prompt),
        "neededExperience": extract_years_of_experience(prompt),
        "jobEndDate": extract_job_end_dates(prompt),
        "company": extract_company_names(prompt),
        "city": cities,
        "country": countries,
        "languages": extract_languages(prompt)
    }

    return json.dumps({
        "job": job
    })
