import re
import difflib
import nltk
import threading
import os
from .constants import SKILLS, STOPWORDS

# Constants
SIMILARITY_THRESHOLD = 0.8

cs_keywords = [
    'computer science',
    'computer engineering'
    'cs',
    'software engineering',
    'information technology'
    'information systems',
    'informatics'
]

# Define lists of keywords for different education levels
bachelor_keywords = ['bachelor', "b.sc", "bsc", "university"]
master_keywords = ['master', "m.sc", "msc"]
phd_keywords = ['phd', 'doctorate', 'doctoral', 'dphil']
# Compile regular expressions for matching keywords
bachelor_regex = re.compile(r'\b(?:' + '|'.join(bachelor_keywords) + r')\b', re.IGNORECASE)
master_regex = re.compile(r'\b(?:' + '|'.join(master_keywords) + r')\b', re.IGNORECASE)
phd_regex = re.compile(r'\b(?:' + '|'.join(phd_keywords) + r')\b', re.IGNORECASE)

# Regular expression pattern to match lines containing the word "years" and optionally "of experience"
years_pattern = r'.*years?(\s*of experience)?.*$'


def remove_stopwords(text):
    """
    Remove stopwords from the text

    Args:
        text (str): The text to remove stopwords from

    Returns:
        str: The text with stopwords removed
    """
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.lower() not in STOPWORDS]
    
    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

def extract_skills_parallel(processed_words, similarity_threshold, num_threads):
    """
    Extract skills from the text using multiple threads

    Args:
        processed_words (list): The list of words to extract skills from
        similarity_threshold (float): The similarity threshold
        num_threads (int): The number of threads to use

    Returns:
        list: The list of extracted skills
    """
    # Define worker function
    def worker(words, start, end, extracted_skills):
        for i in range(start, end):
            word = words[i]
            max_similarity_score = 0
            max_similarity_skill = None
            
            # Get the most similar skill to the current word
            for skill in SKILLS:
                similarity_score = difflib.SequenceMatcher(None, word.lower(), skill.lower()).ratio()
                if similarity_score > max_similarity_score:
                    max_similarity_score = similarity_score
                    max_similarity_skill = skill
            
            # Add the skill to the list if the similarity score is above the threshold
            if max_similarity_score >= similarity_threshold:
                extracted_skills.append(max_similarity_skill)

    # Split the word list into chunks for each thread
    chunk_size = len(processed_words) // num_threads
    threads = []
    extracted_skills = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(processed_words)
        thread = threading.Thread(target=worker, args=(processed_words, start, end, extracted_skills))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return extracted_skills

def extract_skills(text, similarity_threshold=SIMILARITY_THRESHOLD):
    """
    Extract skills from the text

    Args:
        text (str): The description of the job to extract skills from
        similarity_threshold (float, optional): The similarity threshold. Defaults to SIMILARITY_THRESHOLD.

    Returns:
        list: The list of extracted skills
    """
    # Tokenize the input text into words
    input_words = remove_stopwords(text).split()
    processed_words = []
    
    # To handle c/c++/c# cases
    for word in input_words:
        if '/' in word:
            parts = word.split('/')
            processed_words.extend(parts)
        else:
            processed_words.append(word)

    # Determine the maximum number of threads based on available CPU cores
    max_threads = os.cpu_count() or 1

    # Extract skills from the input text using multiple threads
    extracted_skills = extract_skills_parallel(processed_words, similarity_threshold, max_threads)

    return extracted_skills

def handle_current_skills(skills, similarity_threshold=SIMILARITY_THRESHOLD):
    """
    Get the most similar skill to the current skills list

    Args:
        skills (list): The list of skills for the current job
        similarity_threshold (float, optional): The similarity threshold. Defaults to SIMILARITY_THRESHOLD.

    Returns:
        list: The list of extracted skills
    """
    extracted_skills = []
    
    for current_skill in skills:
        max_similarity_score = 0
        max_similarity_skill = None
        
        # Get the most similar skill to the current word
        for skill in SKILLS:
            similarity_score = difflib.SequenceMatcher(None, current_skill.lower(), skill.lower()).ratio()
            if similarity_score > max_similarity_score:
                max_similarity_score = similarity_score
                max_similarity_skill = skill
        
        # Add the skill to the list if the similarity score is above the threshold
        if max_similarity_score >= similarity_threshold:
            extracted_skills.append(max_similarity_skill)
    
    return extracted_skills

def extract_years_of_experience(text):
    """
    Extract years of experience from the job

    Args:
        text (str): The description of the job to extract years of experience from

    Returns:
        tuple: The minimum and maximum years of experience
    """
    # Find all lines containing the word "years" and optionally "of experience"
    matching_lines = [line.strip() for line in text.split('\n') if re.match(years_pattern, line, re.IGNORECASE)]

    # Extract numbers from the matching lines
    years_of_experience = []
    for line in matching_lines:
        matches = re.findall(r'\d+', line)
        if matches:
            # Convert the matches to integers and add them to the list
            matches = [int(match) for match in matches]
            years_of_experience.extend(matches)
            
    if years_of_experience:
        max_experience = max(years_of_experience)
        min_experience = min(years_of_experience)
        return (min_experience, max_experience)
    else:
        return None

def extract_education_level(text):
    """
    Extract education level from the text

    Args:
        text (str): The description of the job to extract education level from

    Returns:
        str: The education level
    """
    # Search for education level matches in the text
    if re.search(phd_regex, text):
        return 'PhD'
    elif re.search(master_regex, text):
        return "Master's"
    elif re.search(bachelor_regex, text):
        return "Bachelor's"
    else:
        return None  # No education level found

def extract_is_computer_science(text):
    """
    Extract if computer science is required for this job

    Args:
        text (str): The description of the job

    Returns:
        bool: True if computer science is required, False otherwise
    """
    
    lowercase_job = text.lower()
    for keyword in cs_keywords:
        if keyword in lowercase_job:
            return True
    
    return False

def prepare_job(unstructured_job):
    """
    Convert the unstructured job to structured job

    Args:
        unstructured_job (dict): The unstructured job that was scraped

    Returns:
        dict: The structured job that will be stored in the database
    """
    
    # Check if there is no title for the job then discard it
    title = unstructured_job.get("title", None)
    if not title:
        return None
    
    if unstructured_job.get("jobPlace", None):
        if unstructured_job["jobPlace"] == "On-site":
            unstructured_job["jobPlace"] = "On Site"
            
    structured_job = {
        "jobId": unstructured_job.get("jobId", None),
        "title": title,
        "company": unstructured_job.get("company", ""),
        "jobLocation": unstructured_job.get("jobLocation", ""),
        "type": "Other" if not unstructured_job.get("type", None) else unstructured_job["type"],
        "url": unstructured_job.get("url", ""),
        "description": unstructured_job.get("description", ""),
        "publishedAt": unstructured_job.get("publishedAt", ""),
        "jobPlace": unstructured_job.get("jobPlace", None),
        "numberOfApplicants": unstructured_job.get("numberOfApplicants", None),
        "isActive": True,
        "isScrapped": True
    }
    
    # Prepare the description
    description = unstructured_job["description"].replace(".", "\n")
    
    # Extract the skills from the description
    skills = extract_skills(description)

    # Check if there is any skill found while scraping
    current_skills = unstructured_job.get("skills", None)
    if current_skills:
        # Get the current skills
        skills += handle_current_skills(unstructured_job["skills"])
    
    structured_job["skills"] = list(set(skills))
    
    # Check if there is any years of experience found while scraping
    neededExperience = unstructured_job.get("neededExperience", None)
    if neededExperience:
        structured_job["neededExperience"] = neededExperience
    else:
        # Take the minimum years of experience from the description
        years_of_experience = extract_years_of_experience(description)
        structured_job["neededExperience"] = years_of_experience[0] if years_of_experience else None
    
    # Check if there is education found while scraping
    education = unstructured_job.get("education", None)
    if education and education != "Not Specified":
        structured_job["education"] = unstructured_job["education"]
    else:
        # Take the education level from the description
        education = extract_education_level(description)
        structured_job["education"] = education if education else "Not Specified"
    
    # Set the computer science requirement
    structured_job["csRequired"] = extract_is_computer_science(description)
    
    return structured_job