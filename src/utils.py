# this file we r writing the CODE in a such a way it provide functionality to entire application 
# importing all the important library which is used in this utils file!!
from src.logger import logging
from src.exception import CustomException
import pymysql #this library use to make connection btn python and mysql database
import os,sys
from dotenv import load_dotenv
import pandas as pd
import dill
from sklearn.metrics import classification_report,confusion_matrix,f1_score,recall_score,precision_score,accuracy_score
from sklearn.model_selection import GridSearchCV

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
    

def SaveObject(filepath,object):
    logging.info('Saving the object to Artifact Folder')
    try:
        #checking artifact folder exist or not
        if not os.path.exists('artifacts'):
            os.makedirs('artifacts',exist_ok=True)
        with open(filepath,'wb') as file:
            dill.dump(object,file)

        logging.info('File saved successfully to Artifact Folder: %s', object)
    except Exception as e:
        raise CustomException(e,sys)


#creating a function for training the model

def evaluate_model(x_train, y_train, x_test, y_test, param_grid1, models):
    report = {}  # Storing the result of model in report object
    logging.info('Training the model')
    
    try:
        # Iterating each algorithm object one by one 
        for i in list(models.keys()):  # Key iterating
            model = models[i]  # Iterating and accessing each algorithm object

            # Accessing param_grid value accordingly
            para = param_grid1[i]
            
            # Hyper-tuning of each model using GridSearchCV algorithm
            grid_search = GridSearchCV(estimator=model, param_grid=para, cv=5)  # Return best hyperparameter

            # Training the model using grid_search algorithm
            grid_search.fit(x_train, y_train)

            # Setting best parameters of hyper-tuning to the model
            model.set_params(**grid_search.best_params_)

            # Training the model after finding out best hyperparameters and setting them into model object
            model.fit(x_train, y_train)

            # Testing the data using test data
            y_pred = model.predict(x_test)

            # Evaluating the accuracy of model
            testing_accuracy_model = accuracy_score(y_test, y_pred)

            report[i] = testing_accuracy_model

        return report
    
    except Exception as e:
        raise CustomException(e,sys)
    
    
def LoadObject(filepath):
    try:
        with open(filepath, 'rb') as f:
            obj = dill.load(f)
        return obj
    except Exception as e:
        raise CustomException(e,sys)