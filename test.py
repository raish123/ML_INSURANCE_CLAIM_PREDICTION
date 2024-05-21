#this file we are creating for testing the code is it working properly or not!!
# so calling the module
from src.loggers import logging
from src.exception import CustomException
import os,sys


def main():
    try:
       pass

    except Exception as e:
        raise CustomException(e,sys)



if __name__ == '__main__':
    main()