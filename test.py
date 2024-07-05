#this file we are creating for testing the code is it working properly or not!!
# so calling the module
from src.logger import logging
from src.exception import CustomException
import os,sys
from src.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.components.data_transformation import DataTransformation,DataTransformationConfig
from src.components.model_trainer import ModelTrainer,ModelTrainerConfig


def main():
    try:
       #creating an object of DataIngestion class
       di = DataIngestion()
       raw_path,train_path,test_path = di.initialize_data_ingestion()

       #creating Datatransformation class object
       dt = DataTransformation()
       train_array,test_array = dt.InitiateDataTransformation(raw_path,train_path,test_path)

       #creating an object of ModelTrainer class
       mt = ModelTrainer()
       mt.initialize_model_training(train_array,test_array)

    except Exception as e:
        raise CustomException(e,sys)



if __name__ == '__main__':
    main()