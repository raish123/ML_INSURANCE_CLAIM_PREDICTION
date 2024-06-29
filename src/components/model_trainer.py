# this file we r using for training the model and finding out which algorithm is suitable for this dataset and saving those model file to pickle format

#importing all the important libraries which is used in the training of the model!!!
import pandas as pd,numpy as np,sklearn
from sklearn.model_selection import train_test_split #this class we used to bifurgate the dataset for training and testing purpose
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
#RFT classifier algorithm is part of ensembling technique working on bagging Mechanism of boot stamping techniqe
from sklearn.ensemble import RandomForestClassifier
#Now calling Classification algorithm of boosting techinique(is also part of ensemble technique) divide into 3 type of algorithm
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier
from xgboost import XGBClassifier
#Now calling the support vector machine algorithm creating a boundry layer or hyperplane which seprate the class of output variable
#hyperplane are 2 type 1)linear sepratable hyperplane b) non linear sepratable hyperplane
from sklearn.svm import LinearSVC,SVC #SVC class we used if datapoint are not linear sepratable
import os,sys
from src.logger import logging
from src.exception import CustomException
from src.utils import SaveObject,evaluate_model
from sklearn.model_selection import GridSearchCV
#for evaluating the accuracy of model we r using
from sklearn.metrics import classification_report,confusion_matrix,f1_score,recall_score,precision_score,accuracy_score
from dataclasses import dataclass
#here we r storing the best model file to artifact folder  so we have define the path of model as a class variable
#this class variable we gonna initialize into object in another class

#creating a class to define the path where to store the best model file
@dataclass
class ModelTrainerConfig():
    model_path = os.path.join('artifacts','model.pkl')


#creating another class to perform the training model task
class ModelTrainer():
    #creting constructor class to define object variable in it and also we can define to initialize the ModelTrainerConfig class object
    def __init__(self):
        self.model_filepath_obj = ModelTrainerConfig()

    
    #creating another object to method to initialize the model training
    def initialize_model_training(self,train_array,test_array):
        logging.info('Here We Are Starting The training Model with multiple Classification ALGORITHM')
        try:
            logging.info('Bifurgating the Train and Test Array Object file')
            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            logging.info('Bifurgation of train and test Array Done')

            logging.info('Initializing The training Model')

            models = {
                'LogisticRegression':LogisticRegression(),
                'DecisionTreeClassifier':DecisionTreeClassifier(),
                'RandomForestClassifier':RandomForestClassifier(),
                'AdaBoostClassifier':AdaBoostClassifier(),
                'GradientBoostingClassifier':GradientBoostingClassifier(),
                'XGBClassifier':XGBClassifier(),
                'SVC': SVC()   
            }

            logging.info('Classification ALgorithm We are passing Hyperparameter in it so That we can Best Accuracy OutCome From It')

            #that tuning we r achieving from GridSearch Cv class of sklearn package

            param_grid = {
                'DecisionTreeClassifier': {
                    'class_weight': ['balanced'],
                    'criterion': ['gini', 'entropy'],
                    #'splitter': ['best', 'random'],
                    'max_depth': [2,4],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2],
                    'max_features': ['auto', 'sqrt', 'log2'],
                    
                },
                'RandomForestClassifier': {
                    'class_weight': ['balanced'],
                    'n_estimators': [10],
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [2,4],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                    # 'max_features': ['auto', 'sqrt', 'log2'],
                    # 'bootstrap': [True, False],
                },
                'AdaBoostClassifier': {
                    'estimator': [None],  # Corrected parameter name
                    'n_estimators': [10],
                    'learning_rate': [0.1, 0.5, 1.0],
                    'algorithm': ['SAMME'],
                },
                'GradientBoostingClassifier': {
                    #'loss': ['deviance', 'exponential'],
                    'learning_rate': [0.05, 0.1, 0.2],
                    'n_estimators': [10],
                    'subsample': [0.8, 1.0],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2],
                    'max_depth': [3, 5],
                    'max_features': ['auto', 'sqrt', 'log2'],
                },
                'XGBClassifier': {
                    'learning_rate': [0.01, 0.05, 0.1],
                    'n_estimators': [10],
                    'max_depth': [3, 5, 7],
                    #'min_child_weight': [1, 3, 5],
                    #'subsample': [0.8, 1.0],
                    #'colsample_bytree': [0.8, 1.0],
                    #'gamma': [0, 0.1, 0.2],
                    'reg_alpha': [0, 0.5, 1],
                    #'reg_lambda': [0, 1, 2],
                },
                'SVC': {
                    'C': [0.1, 1, 10],
                    'kernel': ['linear', 'rbf', 'poly'],
                    'gamma': ['scale', 'auto', 0.1, 1],
                    # 'degree': [2, 3, 4],
                    # 'coef0': [0.0, 0.1, 1.0],
                    # 'shrinking': [True, False],
                    # 'probability': [True, False],
                },
                'LogisticRegression': {
                    'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear', 'saga'],
                    'class_weight': ['balanced'],
                    #'max_iter': [100, 200, 500, 1000]  # Added max_iter parameter with higher values
                }
            }

            

            #now starting the training in utils file passing the parameter 
            #from this file to utils taking out best model list from it

            model_result:dict = evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,param_grid1=param_grid,models=models)

            #now sorting the best score coming out from the result object
            best_model_score = max(sorted(model_result.values()))
            best_model_name = list(model_result.keys())[list(model_result.values()).index(best_model_score)]

            # Retrieve the best model based on the name
            best_model = models[best_model_name]

            
            if best_model_score>=0.8:
                logging.info('No Best Model Found')
            
            logging.info(f"Best Model Found the Name of Model is {best_model} and score of model is {best_model_score}")

            SaveObject(
                filepath = self.model_filepath_obj.model_path,
                object=best_model
            )

            logging.info('Saving the Best model\n%s',best_model)





        except Exception as e:
            raise CustomException(e,sys)
