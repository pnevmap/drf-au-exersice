
# a django rest framework + aurelia.io exercise  
#### Backend
Endpoints based on Django Rest Framework   
**GET documents/**   
**GET documents/<url>** with optional query string parameter revision  (eg documents/some-url/doc1.doc/?revision=1)
	
**GET documents/<url>/revisions**  
**POST documents/**, accepting a document  model like {url:string, file:data }  
**PUT documents/**, accepting a document  model like {url:string, file:data }  
**PUT documents/<url>**, accepting a model { file:data }  
  
All the above endpoints require authentication that could happen at the endpoints bellow  
**GET, POST /api-auth/login** (and GET /api-auth/logout)   
The authentication is Session based (the CRSF token functionallity has been retained)   
Apart from the authentication, object level permissions is implemented in order to avoid user interaction with entities they don't own
  
The source of the backend can be found in the folder versioning  
  
#### Frontend  
A web application based on aurelia.io   
The web app, responds on /static/index.html and reuses the Django's login screen  
Sources for the web app can be found in the folder versioning-ui, however, the compiled files has been copied into the versioning/static folder  
  
  
### Prerequisuites  
* Python 3.8 (e.g. for MacOs execute: `brew install python@3.8`)  
  
### How to run manually
move to the directory drf-au-exersice folder and execute the following commands in a cmd window:
```
python -m venv venv 
venv\Scripts\activate 
pip install -r requirements.txt
### there is already an admin@password123 user in the db, you can create more:
python manage.py createsuperuser --username <your-user-name>  --email foo@foo.foo 
python manage.py makemigrations
python manage.py migrate
python manage.py test versioning
python manage.py runserver
```

### Backend test coverage
There is coverage for the models as well as the api endpoints. 
The model tests are asserting their overriden methods, the computed properties, and their custom methods
The api tests are performing api calls against set up data and then they assert the responses (or vice versa, they perform api calls and they assert the data in the db)
Isolated unit tests for the viewsets as can be considered usufull

### Frontend test coverage
yet to be implemented
 
### Frontend know issues
Missing Pub/Sub Messaging and Routing functionality that sometimes gives poor navigation experience  

### Build a docker image  
there is a **dockerfile** with which we can create the an image:
navigate to drf-au-exersice folder and in a cmd window run the command:  
```docker build -t drf-au-exersice .```

then create a container and run it:  
```docker run --name drf-au-exersice -d -p 8090:8090 drf-au-exersice```  
  
  
### On a Unix-like system  
Go to the drf-au-exersice folder and execute the following in a Terminal:  
  
```shell  
source deploy+run.sh```  
  
### On Windows  
Go to the drf-au-exersice folder and execute the following in a Command:  
```shell  
deploy+run.cmd  
```
