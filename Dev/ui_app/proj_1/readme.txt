#Setup djongo
pip install pymongo
pip install dnspython
pip install djongo
django-admin startproject proj_1
cd proj_1
python manage.py startapp djangoapp  
python manage.py runserver
pip list

'''''''''
pip               22.3.1
pymongo           4.3.3
dnspython         2.2.1
Django            4.1.3
'''''''''''''

#Commands for djongo but not working
django-admin startproject MongoCRUD
pip install pymongo==3.12.3.
pip install dnspython
pip install djongo
pip install pytz

--latest version of pymongo has an issue with djongo so force version of pymongo=3.12.3 to successfully migrate
python manage.py makemigrations djangoapp
python manage.py migrate