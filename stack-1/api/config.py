import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

GRAYLOG_HOST = os.getenv('GRAYLOG_HOST', 'localhost')
GRAYLOG_PORT = int(os.getenv('GRAYLOG_PORT', 12201))
print(GRAYLOG_HOST,GRAYLOG_PORT)
MONGODB_SETTINGS = {
    'db': 'messages',
    'host': os.getenv('MONGO_URI', 'localhost'),
    'port': int(os.getenv('MONGO_PORT', 27017)),
    'username': os.getenv('MONGO_USERNAME', 'admin'),
    'password': os.getenv('MONGO_PASSWORD', 'admin'),
    'connect': True
}

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 30)))
