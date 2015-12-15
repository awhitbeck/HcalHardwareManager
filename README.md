# HCal Hardware Manager

The goal of this django application is to provide a framework for managing HCal 
hardware mappings and frontend configuration constants.  This is a work in progress, 
to say the least.

## Setup 

<pre>
git clone https://github.com/awhitbeck/HcalHardwareManager.git
python manage.py makemigrations qie10peds
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

## Scripts

<pre>clean.py</pre>: Used to remove the 2 primary keys from the data base (QIEcard & BECrate)
and all of their dependents.  Basically, its a fresh start. 

<pre>buildHcal</pre>: Used to initialize the database.  This currently has a number 
of hard coded mappings that are not expected to change, like the ROBOX adapter board 
<-> winchester mapping, but could cause problems in the future.  

Note, if you have already run this, you'll get a conflict when you run it again.  
Instead, you should first run clean.py. 

<pre>dump_emap.py</pre>: Formats the relevant information into a valid E-map which 
can be redirected into a text file.  The tag must be provided through the command
line options '-t'.  See help menu (-h) for details.