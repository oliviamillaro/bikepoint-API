import os
import json
from datetime import datetime
import time
import logging
import requests

logger = logging.getLogger(__name__)

def extract_to_json(url: str, data_dir: str, timestamp: str, max_attempts: int, delay: int):
    """function to extract JSON files from a URL and save to a destination

    Args:
        url (str): API endpoint
        data_dir (str): filepath to save data to
        timestamp (str): timestamp to append to file name
        max_attempts (int): max number of attempts to retry calls
        delay (int): cooldown time between attempts
    """
    #make directory if doesn't exist
    os.makedirs(data_dir,exist_ok=True)

    #build out the file name
    filename = f'{data_dir}/{timestamp}.json'

    #Setting up variables for attempts while loop
    attempts = 1

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
                
                #flag that data was saved successfully for function use
                return True
            
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
            time.sleep(delay)

    #return statement false if the data didn't save
    return False