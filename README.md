# BikePoint API: Extract, Load, and Transform

The goal for the data at the end: Being able to show BikePoint availabilities over time, or the "Popular Times", so you know when you should or shouldn't try to park or rent a bike from a specific BikePoint.

## Extract
The extract script consists of:
- Importing in the necessary libraries
- Defining the datetime of script start and converting that to a string that can be used for filenames
- Creating the log directory and configuring the logging
- Setting up the API endpoint variable as well as variables that can be used for attempt logic
- Making the API call within a while loop, allowing for specific messages or responses based on the response code received back. If successful, the data is saved as a JSON. Also including a try/except in case of successful API call but unsuccessful file saving
- Adding in attempt logic so that a maximum of 3 tries is made, and retries are only sent after 30s cooldown period
