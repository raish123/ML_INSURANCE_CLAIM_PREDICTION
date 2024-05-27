#data_ingestion means reading from differnt source such as server(can be databse or cloud server) and saving raw,test,train data to artifact folder
#so importing all the import library which is used in this file
from src.exception import CustomException
from src.logger import logging
from src.utils import reading_data_server
from sklearn.model_selection import train_test_split
from dataclasses import dataclass #this class we used to initialize class variable using decorator function
import os,sys



#creating class variable to initialize mentioning path of raw,test,train data
@dataclass
class DataIngestionConfig():
    raw_path = os.path.join('artifacts','raw.csv')
    test_path  = os.path.join('artifacts','test.csv')
    train_path = os.path.join('artifacts','train.csv')


#creating another class to start dataingestion process
class DataIngestion():
    #creating constructor method to initialize the object of DataIngestionConfig class
    def __init__(self):
        self.data_ingestion_path_obj = DataIngestionConfig()

    #creating object method to start the data ingestion process
    def initialize_data_ingestion(self):
        logging.info('DataIngestion Process Started')
        try:
            df = reading_data_server()
            logging.info('The data was read successfully\n%s', df.head())
            
            logging.info('Creating artifacts folder')
            os.makedirs(os.path.dirname(self.data_ingestion_path_obj.raw_path),exist_ok=True)

            logging.info('Artifacts folder created successfully')

            df.to_csv(self.data_ingestion_path_obj.raw_path,index=False,header=True)

            logging.info('Raw Data Save into Artifacts Folder')


            logging.info('Raw Data Split into Train and Test data')

            train_df,test_df = train_test_split(df,test_size=0.2,random_state=42)

            logging.info('Raw Data Successfully Split into Train and Test data')

            train_df.to_csv(self.data_ingestion_path_obj.train_path,index=False,header=True)

            logging.info('Train Data Save into Artifacts Folder')

            test_df.to_csv(self.data_ingestion_path_obj.test_path,index=False,header=True)

            logging.info('Test Data Save into Artifacts Folder')

            logging.info('Data Ingestion Done SuccessFully')

            return(
                self.data_ingestion_path_obj.raw_path,
                self.data_ingestion_path_obj.train_path,
                self.data_ingestion_path_obj.test_path
            )

        except Exception as e:
            raise CustomException(e,sys)
