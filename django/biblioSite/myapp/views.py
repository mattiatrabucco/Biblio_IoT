from datetime import datetime
from django.http import HttpResponse
from django.template import loader


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.contrib.auth.decorators import login_required

from .models import TessereUnimore

#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the ecommerce index.")

def register(request):
    template = loader.get_template('register.html')
    context = {}

    try:
        mail = request.POST['mail']
        card_id = request.POST['card_id']
        psw = request.POST['password']
        print(mail)
        print(card_id)
        print(psw)
    except (KeyError):
        # GET
        return HttpResponse(template.render({ 'first': True }, request))
        #return HttpResponse("Errore utente!")
    
    if len(mail) < 3:
        return HttpResponse(template.render({ 'errore': True }, request))
    if len(psw) < 6:
        return HttpResponse(template.render({ 'errore': True }, request))
    
    try:
        utente = TessereUnimore.objects.get(mail=mail)
        if utente.id_tessera == card_id:
            utente.password=psw
            utente.save()
            return HttpResponse(template.render({ 'ok': True }, request))

    except (KeyError, TessereUnimore.DoesNotExist):
        return HttpResponse(template.render({ 'errore': True }, request))
    
    return HttpResponse(template.render({ 'errore': True }, request))


@login_required
def home(request):
    #product_list = Product.objects.all().order_by('name') #.get(pk=post_id) .order_by('-pub_date')[:5]
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))