# this file we used to create log file which is in a format of text 
# this log file we used to track the error and exception occur during run time execution done by interpreters

# so importing all the important libraries which is used in these logging file
import logging
from datetime import datetime
import os

# creating a logs folder that contain .log file in it
folder_name = 'LOGS'
if not os.path.exists(folder_name):
    os.makedirs(folder_name,exist_ok=True)

# creating timestamp for the log files
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#creating a format for log file
log_filename = f"LOGS_FILE_{timestamp}.log"

#creating filepath to store this file into LOGS FOLDER
filepath = os.path.join(folder_name,log_filename)


#creating an object of basicConfig class of logging module
logging.basicConfig(
    filename = filepath,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s -%(lineno)d- %(message)s',  # Log message format

)
