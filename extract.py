#Importing necessary libraries
import os
import json
from datetime import datetime
import time 
import requests

#Making the timestamp to use later for file name, changing it to a string, defining data file name, using os to make file which will only happen when it doesn't exist, bringing all together as a file name
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.json'

#Making the urk a variable in case of needing to change in the future
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
        #Turns response from API into JSON
        data = response.json()

    #Dumps all of the json into the actual file, prints if successful and breaks
        with open(filename,'w') as file:
            json.dump(data, file)

        print(f'File {filename} saved successfully :)')

        break

#If status code not good it will fail, print status code and then break
    elif 300<= status_code <500:
        print(f'API call failed, status code {status_code}')
        break

#If status code is something else e.g. timeout, it gets captured here and will add an attempts and try again in 30 seconds as long as it is under number of max attempt
    else:
        if attempts == max_attempts:
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further.')

        else:
            print(f'Attempt {attempts} failed, status code {status_code}. Trying again.')
        
        attempts+=1
        time.sleep(30)