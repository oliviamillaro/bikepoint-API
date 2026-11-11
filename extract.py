#Importing necessary libraries
import os
import json
from datetime import datetime 
import requests

#Making the timestamp to use later for file name, changing it to a string, defining data file name, using os to make file which will only happen when it doesn't exist, bringing all together as a file name
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.json'

#Making the urk a variable in case of needing to change in the future
url='https://api.tfl.gov.uk/BikePoint/'

#Making the API request
response = requests.get(url)

#Turns response from API into JSON
data = response.json()

#Dumps all of the json into the actual file
with open(filename,'w') as file:
    json.dump(data, file)