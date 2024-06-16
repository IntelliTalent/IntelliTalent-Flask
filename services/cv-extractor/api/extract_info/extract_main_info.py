import re
from .constants import *

name_pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
education_pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
languages_pattern = re.compile(r'\b(?:' + '|'.join([re.escape(lang) for lang in LANGUAGES]) + r')\b', re.IGNORECASE)

def extract_name(cv_text):
    """
    Extract the name from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        str: The name of the person
    """
    name = ""

    # Use regex pattern to find a potential name
    match = re.search(name_pattern, cv_text)
    if match:
        name = match.group()

    return name

def extract_email(cv_text):
    """
    Extract the email from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        str: The email of the person
    """
    email = ""
	
    match = re.search(email_pattern, cv_text)
    if match:
        email = match.group()

    return email

def extract_education(cv_text):
    """
    Extract the education from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        list: The education of the person
    """
    education = []

    # Use regex pattern to find education information
    matches = re.findall(education_pattern, cv_text)
    for match in matches:
        education.append(match.strip())

    return education

def extract_languages(cv_text):
    """
    Extract the languages from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        list: The languages of the person
    """
    return languages_pattern.findall(cv_text)
