from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_ENGINE = os.getenv('POSTGRES_ENGINE')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWD = os.getenv('POSTGRES_PASSWD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
INSTITUTION_CITY = os.getenv('INSTITUTION_CITY')
