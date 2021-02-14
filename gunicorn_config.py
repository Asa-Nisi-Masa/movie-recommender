import os
from dotenv import load_dotenv
load_dotenv()


bind = "0.0.0.0:5000"
workers = 2
threads = 2
timeout = 60
user = os.getenv("DB_USER")
