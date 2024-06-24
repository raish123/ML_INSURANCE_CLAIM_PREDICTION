# this file we r writing the CODE in a such a way it provide functionality to entire application 
# importing all the important library which is used in this utils file!!
from src.logger import logging
from src.exception import CustomException
import pymysql #this library use to make connection btn python and mysql database
import os,sys
from dotenv import load_dotenv
import pandas as pd

#creating an object of load_dotenv class

load_dotenv()  # take environment variables from .env.

#getting database feature from load_dotenv class
db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USERNAME')
db_port  = int(os.getenv('DATABASE_PORT_NO'))
db_host = os.getenv('DATABASE_HOST')
db_pass = os.getenv('DATABASE_PASSWORD')

def reading_data_server():
    logging.info('Creating Connection Between Python and Mysql server')
    try:
        conn = pymysql.connect(user=db_user,
                               database=db_name,
                               port=db_port,
                               host=db_host,
                               password=db_pass)
            
        logging.info('Connection Established Successfully',conn)

        logging.info('Creating Cursor object')
        cur = conn.cursor()

        logging.info('Cursor object Created Successfully this object help to execute the sql query')

        df = pd.read_sql_query('select * from insurance',conn)

        return df

    except Exception as e:
        raise CustomException(e,sys) 