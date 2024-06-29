from .constants import *
from .extract_text import *
from .extract_skills import *
from .extract_experience import *
from .extract_main_info import *


def extract_info(filename):
    """
    Extract info from the cv
    
    Args:
        filename (str): The filename of the cv
        
    Returns:
        dict: The extracted info from the cv
    """
    # Extract the text and all the important sections from the cv
    cv_text = extract_text_from_pdf(filename)
    cv_sections = extract_sections(cv_text)
    
    sections = cv_sections.keys()
    
    # Extract skills from [Skill, Project, Summary]
    # Extract experience from [Experience, Internship]
    # Extract education from [Education]
    # Extract main info from [Summary, Personal]
    # Extract language from [Language]
    # Extract certification from [Certification]
    info = {
        "name": "",
        "email": "",
        "education": [],
        "languages": [],
        "skills": [],
        "projectSkills": [],
        "yearsOfExperience": 0,
        "certifications": [],
    }
    
    for section in sections:
        current_section = cv_sections[section]
        
        if section in ['skill', 'project', 'summary']:
            if section == 'project':
                info['projectSkills'] = extract_project_skills(current_section)
            
            info['skills'] += extract_skills(current_section)
            
        elif section in ['experience', 'internship']:
            info['yearsOfExperience'] += extract_years_of_experience(current_section)
            info['skills'] += extract_skills(current_section)
            
        elif section == 'education':
            info['education'] = extract_education(current_section)
            
        elif section in ['summary', 'personal']:
            info['name'] = extract_name(current_section) if info['name'] == "" else info['name']
            info['email'] = extract_email(current_section) if info['email'] == "" else info['email']
            
        elif section == 'language':
            info['languages'] = extract_languages(current_section)
            
        elif section in ['certification', 'certificate']:
            info['certifications'] = current_section.split('\n')[1:]
    
    info['skills'] = list(set(info['skills']))
    
    return info
