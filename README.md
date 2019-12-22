# YouTube API

## How to run the server
First you have to install all the dependencies that are specified in the requirements.txt file. 

### To run the server:
    python3 manage.py runserver

### Testing the API:
The route of the API is /api, this will return a JSON file with data sorted in reverse chronological order of their publishing time.

### Main Webapp
The main app, i.e. '/' route displays a webpage that has video details posted in the same sorted order as above. Also, pagination is added for better experience.


