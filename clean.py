import django
django.setup()
from qie10peds.models import *
from django.utils import timezone

from hardwareMaps import PMTcoaxMapping,WinchestorConnMapping,QieChannelMapping,TowerMappingA,TowerMappingB


for qc in QIEcard.objects.all() :

    qc.delete()

for bec in BECrate.objects.all() : 

    bec.delete()
