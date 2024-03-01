import logging, os
LOG_LEVEL = logging.DEBUG

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USERNAME')
db_pass = os.getenv('DB_PASSWORD')
profile_db = os.getenv('ProfileDB')

SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{profile_db}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
