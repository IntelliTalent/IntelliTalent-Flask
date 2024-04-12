import difflib, nltk, threading, os
from .constants import *

SIMILARITY_THRESHOLD = 0.8

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

def extract_project_skills(cv_text):
    """
    Extract project skills from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        dict: The project skills of the person with their count
    """
    skill_counts = {}
    skills_list = extract_skills(cv_text, 0.9)

    for skill in skills_list:
        # Update the count for the skill in the dictionary
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
    return skill_counts