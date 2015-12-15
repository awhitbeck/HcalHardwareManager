import django
django.setup()
from qie10peds.models import *
from django.utils import timezone

from hardwareMaps import PMTcoaxMapping,WinchestorConnMapping,QieChannelMapping,TowerMappingA,TowerMappingB

############################################
##### loading QIE card s/n and uniqueIDs
inputQIEdata = open('QIEcardList.txt','r')
QIEinfo = []
first = True

for i in inputQIEdata : 

  if first : 
    first = False
    continue

  cols = i.split(' ')
  tempSN = cols[0]
  tempUniqueID = "{0} {1}".format(cols[1],cols[2])

  QIEinfo.append( { "sn":tempSN , "uniqueID":tempUniqueID } )
############################################

def createCard( tag_ , index_ , sn_ = "101" , uniqueID_ = "0x78000000 0xb9ff7b70" ) : 

    c = QIEcard( uniqueID=uniqueID_ , sn = sn_ )
    c.save()

    for i in range(24) : 

        # print "c.pk",index_
        # print "crate",50+index_/48
        # print "slot",((index_%48)/4) + 1
        # print "fiber",(index_%4)*6+i/4

        be_link = BECrate.objects.filter(crate=50+index_/48,slot=((index_%48)/4)+1,fiber=(index_%4)*6+i/4)[0]

        q = QIE(qie_card=c,be_crate=be_link,tag=tag_,channelIndex=i+1)
        q.save()

        ped = Pedestal(qie=q,
                       tag = tag_ , 
                       commonPedDAC=38,
                       cap1PedDAC=0,
                       cap2PedDAC=0,
                       cap3PedDAC=0,
                       cap4PedDAC=0)

        ped.save()

def displayPedestalSettings( card ) :

    print "commDAC ped1DAC ped2DAC ped3DAC ped4DAC"
    for q in card.pedestal_set.all() :
        print q

def createFEcrate( tag , crateNum , connectedCards=[] ) : 

    slot = []

    for s in range(14) : 
        if s+1 == 8 : continue ## skip ngccm slot
        if s+1 in connectedCards : 
            slot.append( FECrate( tag = t , qie_card = connectedCards[s+1] , crate=crateNum , slot=s+1 ) )
            
    for s in slot : 
        s.save()

def createPMT( tag , phiSect = 1 , connectedCards=[] , boxType_ = PMT.A , side_ = PMT.PLUS ) : 

    qies = connectedCards[0].qie_set.all() | connectedCards[1].qie_set.all() 

    if boxType_ == PMT.A : TowerMapping = TowerMappingA
    if boxType_ == PMT.B : TowerMapping = TowerMappingB

    for pmt in range(24) :

      normalizedPhi = phiSect % 36  

      iPhi_ = normalizedPhi * 2 + TowerMapping[pmt+1][1] 
      if iPhi_ < 0 : iPhi_ += 72

      # grab information from QIE channel mapping about which PMT is connected to which board
      # and which channel.  Note qies is the concatination of two set of 24 qies from different
      # qie cards.
      tempPMT = PMT( qie = qies[QieChannelMapping[pmt+1][1]*24+QieChannelMapping[pmt+1][2]-1] , 
                     tag = t , 
                     side = side_ ,
                     phiSector = (phiSect)/2 + 1 ,
                     WinchestorConn = WinchestorConnMapping[pmt+1][0][0] ,
                     WinchestorPCBconn = WinchestorConnMapping[pmt+1][0][1] ,
                     anode = 1 , iDepth = TowerMapping[pmt+1][3] ,
                     boxPosition = pmt+1 , 
                     boxType = boxType_ , 
                     SigCoaxPMT = PMTcoaxMapping[pmt+1][0][0] , 
                     SigCoaxQIE = PMTcoaxMapping[pmt+1][0][1] , 
                     RefCoaxPMT = PMTcoaxMapping[pmt+1][0][2] , 
                     RefCoaxQIE = PMTcoaxMapping[pmt+1][0][3] , 
                     subDet = "HF" , detID = 0 , 
                     iEta = TowerMapping[pmt+1][0] , iPhi = iPhi_ )
      tempPMT.save()

      tempPMT = PMT( qie = qies[QieChannelMapping[pmt+1][1]*24+QieChannelMapping[pmt+1][3]-1] , 
                     tag = t , 
                     side = side_ ,
                     phiSector = (phiSect/2)+1 ,
                     WinchestorConn = WinchestorConnMapping[pmt+1][1][0] ,
                     WinchestorPCBconn = WinchestorConnMapping[pmt+1][1][1] ,
                     anode = 2 , iDepth = TowerMapping[pmt+1][3]+2 ,
                     boxPosition = pmt+1 , 
                     boxType = boxType_ , #QieChannelMapping[pmt+1][0] ,
                     SigCoaxPMT = PMTcoaxMapping[pmt+1][1][0] , 
                     SigCoaxQIE = PMTcoaxMapping[pmt+1][1][1] , 
                     RefCoaxPMT = PMTcoaxMapping[pmt+1][1][2] , 
                     RefCoaxQIE = PMTcoaxMapping[pmt+1][1][3] , 
                     subDet = "HF" , detID = 0 , 
                     iEta = TowerMapping[pmt+1][0] , iPhi = iPhi_ ) 
      tempPMT.save()

##### - - - - - - - - - - - - - - - 
##### - - - - - - - - - - - - - - - 
##### - - - - - - - - - - - - - - - 
##### - - - - - - - - - - - - - - - 

if len( Tag.objects.filter(name="default") ) == 0 :
    print "creating 'default' tag"
    t = Tag(name="default",pub_date=timezone.now())
    t.save()
else : 
    t = Tag.objects.filter(name="default")[0]

#### create BE links
for c in range( 3 ) :
  for s in range( 12 ) : 
    for f in range( 24 ) : 
      BEC = BECrate( crate = 50+c , slot = s + 1 , fiber = f )
      BEC.save()

#### create dummy QIE cards
for i in range( 144 ) :
    createCard( t , i , QIEinfo[i]["sn"] , QIEinfo[i]["uniqueID"] )

#### dummy PMT boxes
for phi in range(18) : 
    createPMT("default",phi , 
              [QIEcard.objects.all()[8*phi+0],
               QIEcard.objects.all()[8*phi+1] ] , 
              PMT.A , 
              PMT.PLUS
              )

    createPMT("default",phi , 
              [QIEcard.objects.all()[8*phi+2],
               QIEcard.objects.all()[8*phi+3] ] , 
              PMT.B , 
              PMT.PLUS
              )

    createPMT("default",phi , 
              [QIEcard.objects.all()[8*phi+4],
               QIEcard.objects.all()[8*phi+5] ] , 
              PMT.A , 
              PMT.MINUS
              )

    createPMT("default",phi , 
              [QIEcard.objects.all()[8*phi+6],
               QIEcard.objects.all()[8*phi+7] ] , 
              PMT.B , 
              PMT.MINUS
              )
    
#### dummy FE crates    
for i in range(16) : 

    connectedCards = { 3 : QIEcard.objects.all()[9*i+0] , 
                       4 : QIEcard.objects.all()[9*i+1] , 
                       5 : QIEcard.objects.all()[9*i+2] , 
                       6 : QIEcard.objects.all()[9*i+3] , 
                       10: QIEcard.objects.all()[9*i+4] , 
                       11: QIEcard.objects.all()[9*i+5] , 
                       12: QIEcard.objects.all()[9*i+6] , 
                       13: QIEcard.objects.all()[9*i+7] , 
                       14: QIEcard.objects.all()[9*i+8] }

    createFEcrate( t , i , connectedCards )
                       
                       
