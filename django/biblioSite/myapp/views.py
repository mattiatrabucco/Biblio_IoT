from asyncio.windows_events import NULL
from datetime import datetime
from django.http import HttpResponse
from django.template import loader


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import TessereUnimore

#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the ecommerce index.")

def checkHEX(card_id):
    listaHEX=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f',' ']
    for i in card_id:
        if i not in listaHEX:
            return False
    return True

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
    if mail==NULL or psw==NULL or card_id==NULL:
        return HttpResponse(template.render({ 'errore': True }, request))
    if len(mail) != 26 or "@studenti.unimore.it" not in mail : #26 is the number of character of all kind of mail
        return HttpResponse(template.render({ 'errore': True }, request))
    if len(psw) < 6:
        return HttpResponse(template.render({ 'errore': True }, request))
    if checkHEX(card_id) or len(card_id)!=11 :
        return HttpResponse(template.render({ 'errore': True }, request))
    try:
        utente = TessereUnimore.objects.get(mail=mail)
        if utente.id_tessera == card_id:
            utente.password=psw
            utente.save()
            username=mail[0:6]#lo username per il login saranno solo i primi 6 numeri della mail
            user = User.objects.create_user(username,email=mail,password=psw)
            user.save()
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


def logout_view(request):
    logout(request)
    template = loader.get_template('logout.html')
    context = {}
    return HttpResponse(template.render(context, request))
