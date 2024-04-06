import logging, os
LOG_LEVEL = logging.DEBUG

server_ip = os.getenv('SERVER_IP')

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USERNAME')
db_pass = os.getenv('DB_PASSWORD')
profile_db = os.getenv('ProfileDB')

SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{profile_db}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

mongo_host = os.getenv('MONGODB_HOST')
mongo_port = os.getenv('MONGODB_PORT')
mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
mongo_pass = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

MONGODB_URI = f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}'

AVAILABLE_JOB_TITLES = ['ai engineer', 'backend engineer', 'cloud engineer', 'cyber security engineer', 'data analyst', 'data engineer', 'data scientist', 'database administrator', 'database analyst', 'devops engineer', 'front end developer', 'full stack developer', 'it specialist', 'java developer', 'machine learning engineer', 'mobile app developer', 'network administrator', 'network engineer', 'python engineer', 'software developer', 'software engineer', 'support engineer', 'system administrator', 'systems analyst', 'systems engineer', 'ux designer', 'web developer']
AVAILABLE_TITLES_TO_INDEX = {title: i for i, title in enumerate(AVAILABLE_JOB_TITLES)}
INDEX_TO_AVAILABLE_TITLES = {i: title for i, title in enumerate(AVAILABLE_JOB_TITLES)}