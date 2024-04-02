import re
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from .constants import *

def remove_empty_lines(text):
    """
    Remove empty lines from the text

    Args:
        text (str): The cv text

    Returns:
        str: The cv text without empty lines
    """
    # Split the text into lines
    lines = text.split('\n')

    # Remove empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Join the non-empty lines back together
    text_without_empty_lines = '\n'.join(non_empty_lines)
    
    return text_without_empty_lines

def extract_text_from_pdf():
    """
    Extract text from pdf

    Returns:
        str: The text extracted from the pdf
    """
    text = extract_text("cv.pdf")
    text = remove_empty_lines(text)
    
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    final = []
    for line in text.split("\n"):
        line = line.strip()
        
        # Remove special symbols (bullet symbols)
        line = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\u25AA]', '', line)
        
        # Remove extra spaces
        line = re.sub(r'\s+', ' ', line)
        
        final.append(line)
    
    return "\n".join(final)

def extract_sections(cv_text):
    """
    Extract sections from the text

    Args:
        cv_text (str): The cv text

    Returns:
        dict: The extracted sections
    """
    # Extract the following sections:
    # - Education
    # - Experience
    # - Internship
    # - Skill
    # - Language
    # - Project
    # - Summary
    
    sections = {}

    # Split the text into lines
    lines = cv_text.split('\n')
    lines_num = []
    for i in range(len(lines)):
        for title in SECTIONS_TITLES:
            if title.lower() in lines[i].strip().lower() and len(lines[i].strip().lower()) < 30:
                lines_num.append((i, title.lower()))
    
    # Personal section will be the first section
    sections["personal"] = '\n'.join(lines[0:lines_num[0][0]])
    
    # Extract the rest of the sections
    for i in range(0, len(lines_num) - 1):
        sections[lines_num[i][1]] = '\n'.join(lines[lines_num[i][0] + 1:lines_num[i+1][0]])
    
    # Extract last section
    sections[lines_num[-1][1]] = '\n'.join(lines[lines_num[-1][0]:])
    
    return sections
