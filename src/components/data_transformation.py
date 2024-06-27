#in this file we r doing transformation to data means we r filling null value and converting object column to numeric 
#through pipeline and creating preprocessor object file and storiing those preprocessor.pkl file to artifacts folder

#now importing all the important library which is used in this file!!!
import pandas as pd,numpy as np,sklearn
from src.logger import logging
from src.exception import CustomException
import os,sys
from src.components.data_ingestion import DataIngestion
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder
from sklearn.base import BaseEstimator,TransformerMixin #this class we used to creat ac ustom labelencoder class to convert object column to numeric
from sklearn.compose import ColumnTransformer #this class we used to create preprocessor object -->that do converting as well as scaling
from dataclasses import dataclass #this class we used to defined a class variable
from src.utils import SaveObject


#creating a data_transformation_config class in which we r defining the path of preprocessor obj as a class variable in it by using dataclass along with decorators function
@dataclass
class DataTransformationConfig():
    preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

class CustomLabelEncoder(BaseEstimator,TransformerMixin):
    #creating constructor method run automatically when we create this class object
    def __init__(self):
        pass
    #creating fit object method to initialize input variable and output variable to be none
    def fit(self,x,y=None):
        return self
    #creating transform method to convert object column to numeric
    def transform(self,x,y=None):
        #creating 2d empty numpy array object
        x_encoded = np.empty(x.shape,dtype='object')
        #looping through each column of input variable
        for i in range(x.shape[1]):
            #creating labelencoder class object
            le = LabelEncoder()
            x_encoded[:, i] = le.fit_transform(x_encoded[:, i])
        return x_encoded



#now creating another class to perform datatransformation !!!
class DataTransformation():
    #creating a constructor to initialize DataTransformationConfig class object in it
    def __init__(self):
        self.preprocessor_obj = DataTransformationConfig()

    #creating another object method to create a pipeline to do transformation step byt step
    def get_data_transformation(self):
        logging.info('Now doing Data Transformation Through Pipeline')
        try:
            logging.info('From DataIngestion Class Object and accessing raw data path')
            di = DataIngestion()
            raw_path,_,_ = di.initialize_data_ingestion() #calling initialize_data_ingestion method of DataIngestion class
            logging.info('SuccessFully getting raw data filepath from DataIngestion class')
            df = pd.read_csv(raw_path)
            #selecting input and output variable df object
            target_output = 'insuranceclaim'
            x = df .drop(target_output,axis=1) #must be 2d in nature
            y = df[target_output]              #must be 1d in nature
            logging.info('Selecting numeric feature and categorical feature from input variable')
            numeric_column = x.select_dtypes(exclude='object').columns.to_list()
            categorical_column = x.select_dtypes(include='object').columns.to_list()
            logging.info('Numeric Feature\n%s',numeric_column)
            logging.info('Categorical Feature\n%s',categorical_column)

            #creating numericpipeline object by using Pipeline class of sklearn
            num_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')), #this step we fill null value by median
                ('scaling',StandardScaler(with_mean=False)) #this step convert all numeric unit into single unit
            ])
            logging.info('Numeric Pipeline Object\n%s',num_pipeline)

            #creating categoricalpipeline object by using Pipeline class of sklearn
            cat_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),#fill the null value by mode or most frequent value
                ('encoder',CustomLabelEncoder()),#converting object column to numeric column
                ('scaling',StandardScaler(with_mean=False)) #this step convert all numeric unit into single unit
            ])

            logging.info('Categorical Pipeline Object\n%s',cat_pipeline)

            logging.info('combining both pipeline to create preprocessor object using Columtransformer class')
            #combining both pipeline to create preprocessor object using Columtransformer class
            preprocessor = ColumnTransformer(transformers=[
                ('numeric_pipeline',num_pipeline,numeric_column),
                ('categorical_pipeline',cat_pipeline,categorical_column)
            ])
            logging.info('Preprocessor Object\n%s',preprocessor)

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    #creating another object method to start initiating the data transformation on tain and test df object
    def InitiateDataTransformation(self,raw_path,train_path,test_path):
        logging.info('Now Initiating Data Transformation on Train and Test Data')
        try:
            logging.info('Reading train and test Data Using Pandas Library')
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info('Selecting Input and Output Variable From train_data and test_data')
            target = 'insuranceclaim'

            train_data_input_feature = train_data.drop(target,axis=1)
            train_data_output_feature = train_data[target]

            test_data_input_feature = test_data.drop(target,axis=1)
            test_data_output_feature = test_data[target]

            #calling preprocessor object
            preprocessor_obj = self.get_data_transformation()

            logging.info('Now using Preprocessor object came from Column Transformer and applying to train_input_feature and test_input_feature\nScaling we do Only on Input Variable')
            
            input_feature_train_array = preprocessor_obj.fit_transform(train_data_input_feature) #convert into 2d numpy array object
            input_feature_test_array = preprocessor_obj.transform(test_data_input_feature)       #convert into 2d numpy array object

            logging.info('Combining  input feature train array with train_data_output_feature---->to train_numpy_array')
            train_numpy_array = np.c_[input_feature_train_array,np.array(train_data_output_feature)]

            logging.info('Combining  input feature test array with test_data_output_feature---->to test_numpy_array')
            test_numpy_array = np.c_[input_feature_test_array,np.array(test_data_output_feature)]

            logging.info('Saving the preprocessor Object to Artifact folder as Pickle Format')
            SaveObject(
                filepath = self.preprocessor_obj.preprocessor_path,
                object=preprocessor_obj
            )


            return(
                train_numpy_array,
                test_numpy_array
            )

        except Exception as e:
            raise CustomException(e,sys)
