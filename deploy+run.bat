# cd to the propylon folder>
python -m venv venv
venv\Scripts\activate

install requirements.txt
python manage.py createsuperuser --username panos  --email foo@foo.foo
python manage.py makemigrations
python manage.py migrate
python manage.py test versioning
python manage.py runserver