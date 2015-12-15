import django
django.setup()
from qie10peds.models import *
from django.utils import timezone

from hardwareMaps import PMTcoaxMapping,WinchestorConnMapping,QieChannelMapping,TowerMappingA,TowerMappingB

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--tag", dest="tag",
                  help="tag for mapping",default="default")

(options, args) = parser.parse_args()

pmts = PMT.objects.filter(tag__name=options.tag).order_by('qie__qie_card__pk','-WinchestorPCBconn','qie__channelIndex')

print "detid crate slot top/bottom dcc spigot fiber fiber-chan subdet ieta iphi depth"

for pmt in pmts : 

	detid = pmt.detID
	be_crate = pmt.qie.be_crate.crate
	be_slot = pmt.qie.be_crate.slot

	be_fiber = pmt.qie.be_crate.fiber
	be_fiber_chan = pmt.qie.channelIndex%4

	subdet = pmt.subDet
	if pmt.side == PMT.PLUS : 
		ieta = pmt.iEta
	else : 
		ieta = pmt.iEta*(-1)
	iphi = pmt.iPhi
	depth = pmt.iDepth

	print "{0} {1} {2} u 0 0 {3} {4} {5} {6} {7} {8}".format(detid,
															 be_crate,
															 be_slot,
															 be_fiber,
															 be_fiber_chan,
															 subdet,
															 ieta,
															 iphi,
															 depth)

