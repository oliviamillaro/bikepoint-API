#Importing necessary libraries
import os
import json
from datetime import datetime
import time
import logging
import requests

#Making the timestamp to use later for file name, changing it to a string
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

#Like making the directory for data, do the same for logs, and setting up the log file name. Want it to be as early as possible to collect maximum log data
log_dir = 'logs'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

#Defining what we want inside the log file and configuring
logging.basicConfig(
    filename = log_filename,
    format ='%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

#Adding config information and putting it into the logger, and tells us if log file is successfully made
logger = logging.getLogger()
logger.info('Logger successfully initialised.')

#Defining data file name, using os to make file which will only happen when it doesn't exist, bringing all together as a file name
data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.json'

#Making the url a variable in case of needing to change in the future
url='https://api.tfl.gov.uk/BikePoint/'

#Setting up variables for attempts while loop
attempts = 1
max_attempts = 3

#Making the API request, using a while loop
while attempts <= max_attempts:
    response = requests.get(url)
    status_code = response.status_code

#If the status code is around 200 then it is OK and save the response as JSON
    if 200<=status_code<300:
        try:
            #Turns response from API into JSON, and adding try and except in case saving function doesn't work
            data = response.json()

    #Dumps all of the json into the actual file, prints if successful and breaks. If there is an error, added in a nicer error message
            with open(filename,'w') as file:
                json.dump(data, file)
            print(f'File {filename} saved successfully :)')
            logger.info(f'File {filename} saved successfully :)')
        except Exception as e:
            print(f'An error occured when saving the JSON: {e}')
            logger.error(f'An error occured when saving the JSON: {e}')
        break

#If status code not good it will fail, print status code and then break
    elif 300<= status_code <500:
        print(f'API call failed, status code {status_code}')
        logger.error(f'API call failed, status code {status_code}')
        break

#If status code is something else e.g. timeout, it gets captured here and will add an attempts and try again in 30 seconds as long as it is under number of max attempt
    else:
        if attempts == max_attempts:
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further.')
            logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further.')

        else:
            print(f'Attempt {attempts} failed, status code {status_code}. Trying again.')
            logger.error(f'Attempt {attempts} failed, status code {status_code}. Trying again.')
        
        attempts+=1
        time.sleep(30)