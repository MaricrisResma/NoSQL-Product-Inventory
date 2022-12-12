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

----https://www.linkedin.com/learning/django-forms/making-forms-from-scratch?autoSkip=true&autoplay=true&resume=false&u=56968457
First urls.py to create path for homepage and others

Because we are referencing the djangoapp we have to make sure to add it in the settings

views.py
first create view for homepage with request as a parameter
then we want to return a render with the request and url path as parameter
then create similar functions for other views

last step is create corresponding templates for all other views

Django forms

--to run webserver
Python manage.py runserver


https://pymongo.readthedocs.io/en/stable/tutorial.html

bugs 
http://127.0.0.1:8000/order/show/20221105082400 - solved
bug in removing stock - solved


ratings do by http://127.0.0.1:8000/review/show/all manual computation of array - solved
# 

add filter - todo