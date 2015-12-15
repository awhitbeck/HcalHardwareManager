from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class Tag( models.Model ) : 

    name = models.CharField(max_length=200,default="default",unique = True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class QIEcard( models.Model ) :

    uniqueID = models.CharField(max_length=64,unique=True)
    sn = models.IntegerField(unique=True)

    ## ensure that print actually prints something meaningful
    def __str__(self):
        return self.uniqueID


    ## grab crate number attached to a card/tag
    #def getFEcrate( self , tag_ ) : 
    #    hmap = self.get_hmap( tag_ )
    #    return hmap.crate 

    ## grab slot number attached to a card/tag 
    #def getFEslot( self , tag_ ) :
    #    hmap = self.get_hmap( tag_ ) 
    #    return hmap.slot 

    ## method for adding a new row to the hmap table
    ## views should handle the tag so that this function is never called without one
    ## refTag will be used to grab existing slot number -- if empty the latest (in time) row will be used
    #def putFEcrate( self , crate_ , tag_ , refTag = "" ) : 
    #    hmap = self.get_hmap( refTag )
    #    
    #    self.hmap_set.create( crate = crate_ ,
    #                          slot = hmap.slot , 
    #                          tag = tag_ , 
    #                          pub_date = timezone.now() )
    #
    #    self.save()

    ## method for adding a new row to the hmap table
    ## views should handle the tag so that this function is never called without one
    ## refTag will be used to grab existing crate number -- if empty the latest (in time) row will be used
    #def putFEslot( self , slot_ , tag_ , refTag = "" ) :
    #
    #    hmap = self.get_hmap( refTag ) 
    #    
    #    self.hmap_set.create( crate = hmap.crate , 
    #                          slot = slot_ , 
    #                          tag = tag_ , 
    #                          pub_date = timezone.now() )
    #
    #    self.save()

    ## method for adding a new row to the hmap table
    ## views should handle the tag so that this function is never called without one
    #def putFEcrateSlot( self , crate_ , slot_ , tag_ ): 
    #
    #    self.hmap_set.create( crate = crate_ , 
    #                         slot = slot_ , 
    #                         tag = tag_ , 
    #                         pub_date = timezone.now() )
    #
    #    self.save()

    #def dumpEMAP( self ) : 
        
        ## grab hardware information and uHTR mapping information
        ## and format it into a proper EMAP

    #def getPedestals( self , channels ) : 

    #def putPedestals( self , channels , values ) : 

        ## like the putFEcrate etc. functions, this function
        ## should always replicate information that hasn't been provided

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class BECrate( models.Model ) : 

    crate = models.IntegerField(default=1)
    slot = models.IntegerField(default=1)

    fiber = models.IntegerField(default=1)

    def __str__(self):
        return "crate: {0} ; slot: {1} ; fiber: {2}".format(self.crate,self.slot,self.fiber)

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class QIE( models.Model ) : 
    
    ### keys
    qie_card = models.ForeignKey( QIEcard , on_delete = models.CASCADE )
    be_crate = models.ForeignKey( BECrate , on_delete = models.CASCADE )
    tag = models.ForeignKey( Tag , on_delete=models.CASCADE ) #, related_name='FECrateFromTag' ) 

    channelIndex = models.IntegerField(default=1)

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class FECrate( models.Model ) :

    ### keys
    qie_card = models.ForeignKey( QIEcard , on_delete=models.CASCADE )
    tag = models.ForeignKey( Tag , on_delete=models.CASCADE ) #, related_name='FECrateFromTag' ) 

    crate = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)

###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

def validate_coax(value): 
    if value <= 0 or value > 24 : 
        raise ValidationError('{0} is not a valid coax channel (1-24)'.format(value) )
                              
def validate_pmt_pos(value): 
    if value <= 0 or value > 24 : 
        raise ValidationError('{0} is not a valid PMT position (1-24)'.format(value) )
                              
def validate_anode(value): 
    if value <= 0 or value > 2 : 
        raise ValidationError('{0} is not a valid anode (1 or 2)'.format(value) )
                              
def validate_depth(value): 
    if value <= 0 or value > 2 : 
        raise ValidationError('{0} is not a valid depth (1 or 2)'.format(value) )
                              
class PMT( models.Model ) :
                                  
    ## keys
    qie = models.ForeignKey( QIE , on_delete=models.CASCADE ) 
    tag = models.ForeignKey( Tag , on_delete=models.CASCADE ) #, related_name='PMTBoxFromTag' )

    roboxSN = models.IntegerField(default=0)
    phiSector = models.IntegerField(default=0)

    WinchestorConn = models.IntegerField(default=0)

    TOP = 'top'
    BOTTOM = 'bot'
    QIEconn = ( ( TOP , 'top' ) , ( BOTTOM , 'bot' ) )
    WinchestorPCBconn = models.CharField(max_length=3,default=0,choices=QIEconn)

    PLUS = 'plus'
    MINUS = 'minus'
    HFsides = ( ( PLUS , 'plus' ) , ( MINUS , 'minus' ) )
                              
    side = models.CharField(max_length=5,default=PLUS,choices=HFsides)
                              
    anode = models.IntegerField(default=1,validators=[validate_anode])
                              
    boxPosition = models.IntegerField(default=0,validators=[validate_pmt_pos])
    SigCoaxPMT = models.IntegerField(default=0,validators=[validate_coax])
    RefCoaxPMT = models.IntegerField(default=0,validators=[validate_coax])
    SigCoaxQIE = models.IntegerField(default=0,validators=[validate_coax])
    RefCoaxQIE = models.IntegerField(default=0,validators=[validate_coax])
                              
    A = 'A'
    B = 'B'
    boxTypes = ( ( A , 'A' ) , ( B , 'B' ) )
    boxType = models.CharField(max_length=1,default=A,choices=boxTypes)

    detID = models.IntegerField(default=0)    
    subDet = models.CharField(max_length=20,default="HF")
    iEta = models.IntegerField(default=0) 
    iPhi = models.IntegerField(default=0)
    dPhi = models.IntegerField(default=2)
    iDepth = models.IntegerField(default=1,validators=[validate_depth])

    def __str__( self ) :
        return "phi sector - {0}\n s/n - {1}".format(self.phiSector,self.roboxSN)
                              
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class Pedestal( models.Model ) :

    ## keys
    qie = models.ForeignKey( QIE , on_delete=models.CASCADE )
    tag= models.ForeignKey( Tag , on_delete=models.CASCADE ) #, related_name='PedestalFromTag' )

    def __str__( self ) :
        return "{0} {1} {2} {3} ".format(self.commonPedDAC,self.cap1PedDAC,self.cap2PedDAC,self.cap3PedDAC,self.cap4PedDAC)

    commonPedDAC = models.IntegerField(default=38)
    cap1PedDAC   = models.IntegerField(default=0)
    cap2PedDAC   = models.IntegerField(default=0)
    cap3PedDAC   = models.IntegerField(default=0)
    cap4PedDAC   = models.IntegerField(default=0)

# Create your models here.
