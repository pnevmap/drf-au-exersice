# a django rest framework + aurelia.io exercise
Backend endpoints
Some endpoints based on Django Rest Framework 
GET documents/ 
GET documents/<url> with optional query string parameter revision
GET documents/<url>/revisions
POST documents/, accepting a document  model like {url:string, file:data }
PUT documents/, accepting a document  model like {url:string, file:data }
PUT documents/<url>, accepting a model { file:data }

All the above endpoints required authentication that could happen at the endpoints bellow
GET, POST /api-auth/login (and GET /api-auth/logout) 
The authentication is Session based (the CRSF token functionallity has been retained) 

The source of the backend can be found in the folder versioning

Front end
A web application based on aurelia.io 
The web app, responds on /static/index.html and reuses the Django's login screen
Sources for the web app can be found in the folder versioning-ui, however, the compiled files has been copied into the versioning/static folder


##Prerequisuites
* Python 3.8 (e.g. for MacOs execute: `brew install python@3.8`)

##How to manually  
move to the directory drf-au-exersice folder and execute the following commands in a cmd window:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py createsuperuser --username <your-user-name>  --email foo@foo.foo
python manage.py makemigrations
python manage.py migrate
python manage.py test versioning
python manage.py runserver

### Build a docker image
there is a dockerfile that can create the image:
navigate to drf-au-exersice folder and in a cmd window run the command:
docker build -t drf-au-exersice .
then create a container and run it:
docker run --name drf-au-exersice -d -p 8090:8090 drf-au-exersice


### On a Unix-like system
Go to the drf-au-exersice folder and execute the following in a Terminal:

```shell
source deploy+run.sh
```

### On Windows
Go to the drf-au-exersice folder and execute the following in a Command:
```shell
deploy+run.cmd
```
