#Hangout
The mobile web application on Python/Django/jQuery to organize spontaneous meetings. The interface is in Russian.
It uses Python 2 and Django 1.6.

##Installation instructions
* Change/Add the following variables in settings.py:
    * DATABASES
    * GOOGLE_API_KEY
    * GOOGLE_MAPS_API_KEY
    * LITTLESMS_API_USER
    * LITTLESMS_API_KEY
* Change variable in installation_settings.sh
* Run
```
python manage.py syncdb
python manage.py collectstatic
```

