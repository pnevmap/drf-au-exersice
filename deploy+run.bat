# cd to the drf-au-exersice folder
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python manage.py createsuperuser --username panos  --email foo@foo.foo
python manage.py makemigrations
python manage.py migrate
python manage.py test versioning
python manage.py runserver
