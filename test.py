#this file we are creating for testing the code is it working properly or not!!
# so calling the module
from src.logger import logging
from src.exception import CustomException
import os,sys
from src.components.data_ingestion import DataIngestion,DataIngestionConfig


def main():
    try:
       #creating an object of DataIngestion class
       di = DataIngestion()
       di.initialize_data_ingestion()

    except Exception as e:
        raise CustomException(e,sys)



if __name__ == '__main__':
    main()