from dotenv import load_dotenv,find_dotenv
from os import environ as env
from pathlib import Path  # python3 only
import os


# set path to env file
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path,override=True)

class Config:
    """Set Flask configuration vars from .env file."""

    # Load in enviornemnt variables
    FLASK_APP=os.getenv('FLASK_APP')
    TESTING = os.getenv('TESTING')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')
    FLASK_ENV=os.getenv('FLASK_ENV')

