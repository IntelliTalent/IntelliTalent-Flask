import re
from dataset.dataset import skills, job_titles, countries, locations, job_types, languages
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

def extract_skills(prompt):
    """Extract skills from the given prompt."""
    skill_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(skill) for skill in skills) + r')\b', re.IGNORECASE)
    return skill_pattern.findall(prompt)


def normalize_job_title(input_title):
    """Normalize the user's job title to the canonical form."""
    input_title = input_title.lower()
    for canonical_title, variations in job_titles.items():
        if input_title in variations:
            return canonical_title
    return None

def extract_job_titles(prompt):
    """Extract job titles from the given prompt."""
    words = word_tokenize(prompt)
    job_titles_found = []
    # try with each word in the prompt
    for word in words:
        normalized_title = normalize_job_title(word)
        if normalized_title:
            job_titles_found.append(normalized_title)
    # try with sliding window with 2 words
    for i in range(len(words) - 1):
        normalized_title = normalize_job_title(' '.join(words[i:i+2]))
        if normalized_title:
            job_titles_found.append(normalized_title)
    # try with sliding window with 3 words
    for i in range(len(words) - 2):
        normalized_title = normalize_job_title(' '.join(words[i:i+3]))
        if normalized_title:
            job_titles_found.append(normalized_title)
    return job_titles_found

def extract_locations(prompt):
    """Extract locations from the given prompt."""
    location_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(location) for location in locations) + r')\b', re.IGNORECASE)
    return location_pattern.findall(prompt)

def extract_job_types(prompt):
    """Extract job types from the given prompt."""
    # job_type_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(job_type) for job_type in job_types) + r')\b', re.IGNORECASE)
    extracted_job_types = []
    for canonical_title, variations in job_types.items():
        for variation in variations:
            if variation in prompt:
                extracted_job_types.append(canonical_title)
    return extracted_job_types

def extract_years_of_experience(prompt):
    """Extract years of experience from the given prompt."""
    # Updated regex pattern for years of experience
    years_of_experience_pattern = re.compile(
    # r'\b(\d+)\s*-\s*(\d+)\s*years?\s*of?\s*experience\b|'  # e.g., 1-10 years of experience or 1-10 years experience
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s+years?\s*of?\s*experience\b|'  # e.g., 5 years of experience
    r'\bexperience\s*of\s*((\d+)|(\d+)\s*-\s*(\d+))\s*years?\b|'  # e.g., experience of 5 years
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s*years?\s*experience\b|'  # e.g., 5 years experience
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s*yrs?\s*of?\s*experience\b|'  # e.g., 5 yrs of experience
    r'\bexperience\s*with\s*((\d+)|(\d+)\s*-\s*(\d+))\s*years?\b|'  # e.g., experience with 5 years
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s*yrs?\s*experience\b|'  # e.g., 5 yrs experience
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s*\+\s*years?\s*experience\b|'  # e.g., 5+ years experience
    r'\b((\d+)|(\d+)\s*-\s*(\d+))\s*\+\s*years?\s*of\s*experience\b'  # e.g., 5+ years of experience
    , re.IGNORECASE)
    matches = years_of_experience_pattern.findall(prompt)
    result = []
    for match in matches:
        # # Filter out empty strings and format the range or single year correctly
        cleaned_match = [x for x in match if x]
        result.append(f"{cleaned_match[0]}")
        # if len(cleaned_match) == 2:
        #     result.append(f"{cleaned_match[0]}-{cleaned_match[1]}")
        # elif len(cleaned_match) == 1:
        #     result.append(cleaned_match[0])
        # if(match):  # Filter out empty strings
        #     result.append(match)
    return result

def extract_job_end_dates(prompt):
    """Extract job end dates from the given prompt."""
    job_end_date_pattern = re.compile(
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s+\d{4})?\b|'  # Month Day, Year (Year optional)
        r'\b(?:\d{1,2})/(?:\d{1,2})(?:/\d{2,4})?\b|'  # MM/DD/YYYY or MM/DD/YY (Year optional)
        r'\b(?:\d{1,2})-(?:\d{1,2})(?:-\d{2,4})\b|'  # MM-DD-YYYY or MM-DD-YY (Year optional)
        r'\b(?:\d{1,2})\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*(?:\d{4})?\b|'  # Day Month Year (Year optional)
        r'\b(?:\d{4})-(?:\d{2})-(?:\d{2})\b',  # YYYY-MM-DD
        re.IGNORECASE
    )
    return job_end_date_pattern.findall(prompt)

def extract_countries_cities(prompt):
    """Extract countries using NLTK's named entity recognition."""
    sentences = nltk.sent_tokenize(prompt)
    countries = []
    cities = []
    for sentence in sentences:
        chunks = ne_chunk(pos_tag(word_tokenize(sentence)))
        for chunk in chunks:
            if hasattr(chunk, 'label') and chunk.label() == 'GPE':  # GPE: Geopolitical Entity
                location = ' '.join(c[0] for c in chunk)
                if is_country(location):
                    countries.append(location)
                else :
                    cities.append(location)
    return countries, cities

def is_country(location):
    """Helper function to determine if a location is a country."""
    # This function can be expanded with a comprehensive list of countries
    return location in countries

def extract_languages(prompt):
    """Extract languages from the given prompt."""
    language_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(language) for language in languages) + r')\b', re.IGNORECASE)
    return language_pattern.findall(prompt)

def extract_company_names(prompt):
    """Extract company names using NLTK's named entity recognition."""
    sentences = nltk.sent_tokenize(prompt)
    company_names = []
    for sentence in sentences:
        chunks = ne_chunk(pos_tag(word_tokenize(sentence)))
        for chunk in chunks:
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                company_name = ' '.join(c[0] for c in chunk)
                if company_name not in skills: 
                    company_names.append(company_name) 
    return company_names