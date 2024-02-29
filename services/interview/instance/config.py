import logging, os
LOG_LEVEL = logging.DEBUG

mongo_host = os.getenv('MONGODB_HOST')
mongo_port = os.getenv('MONGODB_PORT')
mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
mongo_pass = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

MONGODB_URI = f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}'
