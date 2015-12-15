import django
django.setup()
from qie10peds.models import *
from django.utils import timezone

c = QIEcard.objects.all()[0]


# Create your tests here.
