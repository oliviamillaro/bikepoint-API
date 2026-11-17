from datetime import datetime
import os
import logging
from dotenv import load_dotenv
#importing a function locally specifying file locatally and then import function name
from modules.extract_function import extract_to_json
from modules.load_function import load_to_s3

#Making the timestamp to use later for file name, changing it to a string
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

#Like making the directory for data, do the same for logs, and setting up the log file name. Want it to be as early as possible to collect maximum log data
log_dir = 'logs'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

#Defining what we want inside the log file and configuring
logging.basicConfig(
    filename = log_filename,
    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

#Adding config information and putting it into the logger, and tells us if log file is successfully made
logger = logging.getLogger()
logger.info('Logger successfully initialised.')

#setting up config for API call
url='https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'
max_attempts = 3

load_dotenv()

#aws access
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')

extract_result = extract_to_json(url, data_dir, timestamp, max_attempts, delay=10)
print(extract_result)

if extract_result:
    # run load to s3
    load_to_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, data_dir)

else:
    logger.info('Extract saved no data, nothing to upload so script killed')