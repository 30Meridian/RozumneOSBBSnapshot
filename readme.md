**SaaS Service for Condominiums** 
   
**Requirements**
- Python3
- Django 1.8.13
- MariaDB 10
- 
  
**Installation:**
The project works on Windows or Linux-like OS. 
Precompiled Windows driver for DB you can find on ***deploy*** folder.   

**How to install:**
1. Firstly install Python 3.4 (https://www.python.org/downloads/release/python-345/)
2. Install MariaDB 10.1 (https://downloads.mariadb.org/)
3. If you have another Python-project, please activate a virtualenv (http://virtualenvwrapper.readthedocs.io/en/latest/)
4. To work with a virtual environmental use a >***workon yourvirtenvname*** command
5. Install wheels from `for_deploy` folder and `gettext`
6. Install requirement packages: ***```pip install -r requirements.txt```***
7. Create a table structure  ***```python manage.py syncdb```***
8. Create default permissions for proxy models ***```python manage.py fix_permissions```***
  
**How to configure the project:**
1. Configuration files placed in ***system/settings*** and have dropped to ***development.py*** (for development purposes) and ***production.py*** (for production). 
  In accordance, when you develop project run server like this: ***```manage.py runserver 127.0.0.1:8000 --settings=system.settings.development```***  
2. Before start configure first a variable: ***URL*** , ***SECRET_KEY***, ***DATABASES***  
3. Run a local server - ***```manage.py runserver 127.0.0.1:8000 --settings=system.settings.development```***  

To work with a virtual environmental use a >***workon yourvirtenvname*** command

**Design**
http://demos.creative-tim.com/light-bootstrap-dashboard-pro/examples/dashboard.html
  
 **NewsLetter**
Module - https://github.com/dokterbob/django-newsletter
Full documentation - http://django-newsletter.readthedocs.io/en/latest/


**Forum**
Read about this module on https://github.com/ellmetha/django-machina#documentation
Full documentation you can find on - https://django-machina.readthedocs.io/en/stable/getting_started.html   


**Production server**
To restart gunicorn on production server user ***systemctl restart gunicorn*** as superuser


