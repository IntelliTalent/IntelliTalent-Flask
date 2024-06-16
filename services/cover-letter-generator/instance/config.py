import logging, os
LOG_LEVEL = logging.DEBUG

SERVER_HOST = os.getenv('SERVER_HOST')

AVAILABLE_JOB_TITLES = ['ai engineer', 'backend engineer', 'cloud engineer', 'cyber security engineer', 'data analyst', 'data engineer', 'data scientist', 'database administrator', 'database analyst', 'devops engineer', 'front end developer', 'full stack developer', 'it specialist', 'java developer', 'machine learning engineer', 'mobile app developer', 'network administrator', 'network engineer', 'python engineer', 'software developer', 'software engineer', 'support engineer', 'system administrator', 'systems analyst', 'systems engineer', 'ux designer', 'web developer']
AVAILABLE_TITLES_TO_INDEX = {title: i for i, title in enumerate(AVAILABLE_JOB_TITLES)}
INDEX_TO_AVAILABLE_TITLES = {i: title for i, title in enumerate(AVAILABLE_JOB_TITLES)}