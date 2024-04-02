import re
from datetime import datetime

date_pattern = r'(((Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)|(\d{1,2}\/){0,2})[- ]?\d{4}?)'

def parse_date(date_str):
    """
    Parse a date string into a datetime object

    Args:
        date_str (str): The date string to parse

    Returns:
        datetime: The parsed date
    """
    if 'current' in date_str.lower() or 'present' in date_str.lower() or 'now' in date_str.lower():
        return datetime.now().date()
    
    # Convert all months
    date_str = date_str.replace(r'Jan(uary)?', 'January')
    date_str = date_str.replace(r'Feb(ruary)?', 'February')
    date_str = date_str.replace(r'Mar(ch)?', 'March')
    date_str = date_str.replace(r'Apr(il)?', 'April')
    date_str = date_str.replace(r'May', 'May')
    date_str = date_str.replace(r'June?', 'June')
    date_str = date_str.replace(r'July?', 'July')
    date_str = date_str.replace(r'Aug(ust)?', 'August')
    date_str = date_str.replace(r'Sep(tember)?', 'September')
    date_str = date_str.replace(r'Oct(ober)?', 'October')
    date_str = date_str.replace(r'Nov(ember)?', 'November')
    date_str = date_str.replace(r'Dec(ember)?', 'December')
    
    try:
        return datetime.strptime(date_str, '%m/%Y').date()
    except ValueError:
        pass
    
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        pass
    
    try:
        return datetime.strptime(date_str, '%B %Y').date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, '%Y').date()
    except ValueError:
        pass

    return None

def calculate_years_of_experience(start_date, end_date):
    """
    Calculate the years of experience between two dates

    Args:
        start_date (datetime): The start date
        end_date (datetime): The end date

    Returns:
        float: The years of experience
    """
    years_of_experience = (end_date.year - start_date.year) + (end_date.month - start_date.month) / 12
    return years_of_experience

def extract_years_of_experience(cv_text):
    """
    Extract the years of experience from the cv

    Args:
        cv_text (str): The text of the cv

    Returns:
        float: The years of experience
    """
    
    def preprocess(cv_text):
        # Preprocess the cv_text
        cv_text = cv_text.replace("–", "-")

        # Convert "Month1-Month2 Year" to "Month1 Year - Month2 Year"
        cv_text = re.sub(r'(\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\w*)-(\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\w*) (\d{4})', r'\1 \5 - \3 \5', cv_text)

        return cv_text

    total_years = 0

    cv_text = preprocess(cv_text)

    # Attempt to match date ranges in the format "start_date - end_date"
    matches = re.finditer(r'({})\s*-\s*({})'.format(date_pattern, date_pattern), cv_text)
    for match in matches:
        dates = match.group(0).split('-')
        start_date = parse_date(dates[0].strip())
        end_date = parse_date(dates[1].strip())

        if start_date and end_date:
            total_years += calculate_years_of_experience(start_date, end_date)
    
    # Attempt to match date ranges in the format "start_date - Present or Current"
    matches = re.finditer(r'({})\s*-\s*.*([Pp]resent|[Cc]urrent|[Nn]ow).*'.format(date_pattern), cv_text)
    for match in matches:
        dates = match.group(0).split('-')
        start_date = parse_date(dates[0].strip())
        end_date = parse_date(dates[1].strip())

        if start_date and end_date:
            total_years += calculate_years_of_experience(start_date, end_date)

    return total_years
