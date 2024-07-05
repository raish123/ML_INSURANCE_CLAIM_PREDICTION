#in this file we create a pipeline from web application whaterver inputs coming from it we first
#do preprocessing to that datapoint by using preprocessor.pkl file then we apply bestmodel.pkl file for prediction
#and finally we return the result to the web application

#importing all the important library which is used to create this file
import os,sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import SaveObject,dill,LoadObject

#first creating a predict pipeline class in which we load pickle file and do transformation and prediction in it
class PredictPipeline():
    #creating a empty constructor method
    def __init__(self):
        pass
    #creating another object method which will load the pickle files
    def Predict(self,features):
        logging.info('Here we Are unpickling the preprocessor and model file')
        try:
            #loading the preprocessor file
            preprocessor_filepath = 'artifacts\preprocessor.pkl'
            model_filepath = 'artifacts\model.pkl'

            logging.info('Initiate unpicking files')

            preprocessor_obj = LoadObject(preprocessor_filepath)
            model_obj = LoadObject(model_filepath)

            logging.info('Unpickling Of file Done Successfully')

            logging.info('Now Doing Transformation And Scaling of new Feature Coming From WebPage\nThen Doing Prediction')
            transformed_features = preprocessor_obj.transform(features)

            prediction = model_obj.predict(transformed_features)

            return prediction

           
        except Exception as e:
            raise CustomException(e,sys)


#Creating Another Custom Class so that whatever input coming from webpage
#storing ointo structured format mei

class CustomData():
    # creating constructor method to initialize the variable or attributes in it
    def __init__(self,age:int,sex:int,bmi:float,children:int,smoker:int,region:int,charges:float):

        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.region = region
        self.charges = charges
        

    #creating another object method to convert above data into df object
    def get_data_df(self):
        try:
            custom_dict = {
                'age':[self.age],
                'sex':[self.sex],
                'bmi':[self.bmi],
                'children':[self.children],
                'smoker':[self.smoker],
                'region':[self.region],
                'charges':[self.charges]
            }

            df = pd.DataFrame(custom_dict)
            return df 
        except Exception as e:
            raise CustomException(e,sys)


