import os, pymysql,logging, time
from mysql.connector import connect
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'database': os.getenv('DB_NAME'),
    'ssl_ca': os.getenv('DB_SSL')  # Update path to your CA certificate
}

def initialize_db():
    return connect(**db_config)