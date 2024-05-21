#this is exception.py file we r creating custom_exception to raise the error message whatever occur during runtime execution done by interpreters

#importing all the important library which is used in this file.
import os,sys
from src.loggers import logging

#I am creating an error message ka format that i want to display during runtime execution exception occur

def get_error_message(error,error_details:sys):
    # error parameter we r getting from Exception class 
    #sys module will have error deatils when execption occur during runtime execution
    # exc_info() built in method of sys module generally we used to get information of error_details rtn 3 paramter of tuple-->type,error_value,info_error
    _,_,exc_tb = error_details.exc_info() 
    filename = exc_tb.tb_frame.f_code.co_filename
    lineno = exc_tb.tb_lineno

    message = f"Error getting in this file {filename} at this line number {lineno} and error message will be {str(error)}"
    return message




#creating custom except class
class CustomException(Exception):
    #creating constructor method for CustomException class
    def __init__(self,error,error_details:sys):
        #inheriting constructor method to get  error from Parent exception class
        super().__init__(error)

        self.error_message = get_error_message(error,error_details=error_details)


    #__str__ is special method  in python which returns string representation of an object
    def __str__(self):
        return self.error_message

