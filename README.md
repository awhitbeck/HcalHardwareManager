# HCal Hardware Manager

The goal of this django application is to provide a framework for managing HCal 
hardware mappings and frontend configuration constants.  This is a work in progress, 
to say the least.

## Setup 

<pre>
git clone https://github.com/awhitbeck/HcalHardwareManager.git
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8080
python buildHcal.py
</pre>

Then go to http://127.0.0.1:8080/admin/

## Database structure

The database structure is defined in qie10peds/models.py 

## Web views

The database structure is defined in qie10peds/models.py 
