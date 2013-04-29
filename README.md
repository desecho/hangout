#Hangout

The web application to organize spontaneous meetings. The interface is in Russian.

##Required packages

* [Python v2.6.5+](http://www.python.org)
* [Django v1.5](http://djangoproject.com)
* [django-annoying v0.7.7+](https://github.com/skorokithakis/django-annoying)
* [littlesms-python](https://github.com/igrishaev/littlesms-python/)
* [python-googl v0.2.2](https://pypi.python.org/pypi/python-googl/0.2.2)

##Used Javascript libraries
* [jQuery v1.9.1](http://jquery.com/)
* [jQuery Mobile v.1.3.1](http://jquerymobile.com/)
* [GMap 3 v.5.0b](http://gmap3.net/en/)
* [Bootstrap v2.3.1](http://twitter.github.com/bootstrap/)

##Used Graphics Packages
* [Font Awesome v3.0.2](http://fortawesome.github.com/Font-Awesome/)

##Installation instructions

* Insert your database settings in settings.py

* You'll need to get the API keys and input them in settings.py

* Run
```
python manage.py syncdb
python manage.py collectstatic
```

