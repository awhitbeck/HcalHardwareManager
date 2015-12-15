from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import *

def index( request ) : 
    
    return HttpResponse("Haha!")
    
def fecrate( request , chosen_tag ) : 

    context = { "cards" : [] }
    cards = QIEcard.objects.all() 
    for card in cards : 
        fecrates = card.fecrate_set.filter(tag__name = chosen_tag)
        for fecrate in fecrates : 

            print fecrate.qie_card.uniqueID,fecrate.crate,fecrate.slot

            context["cards"].append( (fecrate.qie_card.uniqueID,fecrate.crate,fecrate.slot) )
    
    return render( request , 'qie10peds/fecrate.html' , context )

def pmt( request , chosen_tag ) : 

    pmts = PMT.objects.filter(tag__name=chosen_tag).order_by('qie__qie_card__pk','-WinchestorPCBconn','qie__channelIndex')
    #pmts = PMT.objects.filter(tag__name=chosen_tag).order_by('iEta','iPhi')

    context = { "pmts" : [] }
 
    for pmt in pmts :
            context["pmts"].append( pmt )
            
    return render( request , 'qie10peds/pmt.html' , context )

def peds( request , card_pk , chosen_tag ) : 
    
    #if len( QIEcard.objects.filter(pk=card_pk) ) == 0 : 
    #    raise Http404("QIE card not found")

    card = QIEcard.objects.filter(pk=card_pk)[0]

    context = { "uniqueID" : card.uniqueID }
    context["card_pk"] = card_pk 
    context["tag"] = "" #chosen_tag 

    context["index"] = []
    context["commPeds"] = []
    context["cap1Peds"] = []
    context["cap2Peds"] = []
    context["cap3Peds"] = []
    context["cap4Peds"] = []
    
    #for qie in card.pedestal_set.filter(tag=chosen_tag) :
    #    context["index"].append( qie.channelIndex )
    #    context["commPeds"].append( qie.commonPedDAC ) 
    #    context["cap1Peds"].append( qie.cap1PedDAC )
    #    context["cap2Peds"].append( qie.cap2PedDAC )
    #    context["cap3Peds"].append( qie.cap3PedDAC )
    #    context["cap4Peds"].append( qie.cap4PedDAC )

    print context

    return render( request , 'qie10peds/peds.html' , context )

#def editpeds( request ) : 

#    if not 'tag' in request.POST or request.POST['tag'] == "" : 
#        raise Http404("tag is required for upating HMAP")
#    else :

#        for c in 

def edithmap( request ) : 

    if not 'tag' in request.POST or request.POST['tag'] == "" : 
        raise Http404("tag is required for upating HMAP")
    else : 
        
        ## loop over each QIE card in database and check to make sure that the relevant 
        ## information is available in the form, otherwise through a 404 error
        for c in QIEcard.objects.all() : 

            if not 'crate{0}'.format(c.pk) in request.POST or request.POST['crate{0}'.format(c.pk)] == "" :
                raise Http404("crate info missing for {0}".format(c.uniqueID))
            if not 'slot{0}'.format(c.pk) in request.POST or request.POST['slot{0}'.format(c.pk)] == "" :
                raise Http404("slot info missing for {0}".format(c.uniqueID))
            updatedCrate = int(request.POST['crate{0}'.format(c.pk)])
            updatedSlot = int(request.POST['slot{0}'.format(c.pk)])

            c.hmap_set.create( crate = updatedCrate , 
                               slot  = updatedSlot , 
                               tag   = request.POST['tag'] , 
                               pub_date = timezone.now() )

        ## after all information has been retrieved from form, save
        for c in QIEcard.objects.all() : 
            c.save()

    return hmap( request , request.POST['tag'] ) 

# Create your views here.
