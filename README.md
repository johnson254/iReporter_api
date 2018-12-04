IREPORTER
====
Features
===
The users can perform the following functions:

* Register
* Login
* Reset Password
* Register a record or intervition
* Update a record
* Get intervison
* Get red-flag/intervintion by id
* Delete a red-flag/intervision

Prerequisites
----
To run the Api endpoint use either of the following software:
* Postman/Curl - Testing the endpoints
* Text Editor - Making changes in the code base
*  Terminal - Run the api file

----
To Access the enpoint follow the directory.
- To access the endpoints clone the repo and cd into the following directory
* $ cd WeConnect/source/api ```api.py```

Api endpoints
---
```
1. Users 
-  POST /api/v1/auth/register Creates user account
-  POST /api/v1/auth/login Log in user
-  POST /api/v1/auth/logout Logout user
-  PUT /api/v1/auth/reset-password Resets user password


Running the API
---
1. To run the API cd into ```$ cd iReporter```
2. Create a virtual environment to install your dependencies.
* ```virtualenv -p python3 venv``` for mac and linux users
* ```virtualenv venv``` for windows users
3. Activate the virtual environment to install dependecies.
* ```source venv/bin/activate``` for mac and linux users
* ```source venv/scripts/activate``` for windows users
4. Install the requirements
```pip -r requirements.txt``` use the command to install dependecies.(mac,linux,windows)
5. Finally write the following command in your terminal ```python run.py```

Running tests
---
To run the tests assert that the virtual environment is activated:

* Activate virtual env
* Install pip requirements - ```pip -r requirements.txt```
* Run the following command in your terminal ```nosetests```

Built With
---
1. Flask 
2. Json {}

Versioning
---
- Version 0.0.1

Contributing
---
- Contributing to the development of this app is allowed just fork it!!!
  do changes and create a pull request...

Authors
---
* Johnson wambiru

