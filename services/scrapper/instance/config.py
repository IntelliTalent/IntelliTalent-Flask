import logging, os
LOG_LEVEL = logging.DEBUG

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USERNAME')
db_pass = os.getenv('DB_PASSWORD')
structured_jobs_db = os.getenv('StructuredJobsDB')

SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{structured_jobs_db}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

mongo_host = os.getenv('MONGODB_HOST')
mongo_port = os.getenv('MONGODB_PORT')
mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
mongo_pass = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

MONGODB_URI = f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}'

# Constants for the scrapper

# Number of times to try the same query (linkedin gives different results each time)
ROUNDS = 1

# The number of pages to scrape for each search query
PAGES_TO_SCRAPE = 10

# Number of times to retry to connect to the same url
RETRIES = 3
DELAY = 1

JOB_TITLES = ['ai engineer', 'backend engineer', 'cloud engineer', 'cyber security engineer', 'data analyst', 'data engineer', 'data scientist', 'database administrator', 'database analyst', 'devops engineer', 'front end developer', 'full stack developer', 'it specialist', 'java developer', 'machine learning engineer', 'mobile app developer', 'network administrator', 'network engineer', 'python engineer', 'software developer', 'software engineer', 'support engineer', 'system administrator', 'systems analyst', 'systems engineer', 'ux designer', 'web developer']
JOB_LOCATIONS = ['Egypt', 'Saudi Arabia', 'United Arab Emirates', 'Qatar', 'Kuwait', 'Bahrain', 'Oman', 'Jordan', 'Lebanon', 'Iraq', 'Syria', 'Yemen', 'Libya', 'Tunisia', 'Algeria', 'Morocco', 'Sudan', 'Palestine', 'Comoros', 'Djibouti', 'Mauritania', 'Somalia']

# 0: onsite - 1:hybrid - 2:remote - empty:no value
JOB_TYPES = [1, 2, 3, '']

# Max number of days to scrape (take only the last DAYS_TO_SCRAPE days) 
DAYS_TO_SCRAPE = 1
