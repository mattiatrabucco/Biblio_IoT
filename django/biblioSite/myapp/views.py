#from asyncio.windows_events import NULL
from datetime import datetime
from django.http import HttpResponse
from django.template import loader


from django.contrib import admin

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, get_user_model
from .models import Biblioteche, TessereUnimore
import string

def checkHEX(card_id):
    return all(c in string.hexdigits for c in card_id)

#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    elenco_biblio = Biblioteche.objects.all()
    diz_biblio = {} #oggetto da passare all'HTML
    diz_biblio_cap={}
    diz_biblio_count={}
    for biblio in elenco_biblio:
        cap = int((biblio.count / biblio.capienza) * 100)
        diz_biblio[biblio.nome] = cap
        diz_biblio_cap[biblio.nome] = biblio.capienza
        diz_biblio_count[biblio.nome] = biblio.count
        #diz_biblio[biblio.nome] = [cap,biblio.count,biblio.capienza]
        #print(diz_biblio[biblio.nome])
    context = {
        'biblio' : diz_biblio,
        'cap' : diz_biblio_cap, 
        'count':diz_biblio_count
    }
    return HttpResponse(template.render(context, request))

#path('register/', views.register, name='register')
def register(request):
    template = loader.get_template('register.html')

    try:
        email_number = request.POST['email_number']
        card_id = request.POST['card_id']
        psw = request.POST['password']
        #print(mail)
        #print(card_id)
        #print(psw)
    except (KeyError):
        # GET
        return HttpResponse(template.render({ 'first': True }, request))

    # Check email_number:
    if email_number is None or len(email_number) != 6: # EXAMPLE: 123456@studenti.unimore.it
        return HttpResponse(template.render({ 'email_number_error': True }, request))

    # Check password:
    if psw is None or len(psw) < 8: 
        return HttpResponse(template.render({ 'psw_error': True }, request))
    
    # Check card_id:
    card_id = "".join(card_id.split()) # Removes all whitespaces
    card_id = card_id.upper()
    if card_id is None or not checkHEX(card_id) or len(card_id)!=8 :
        return HttpResponse(template.render({ 'card_id_error': True }, request))
    card_id = " ".join(card_id[i:i+2] for i in range(0, len(card_id), 2)) # Reassemble the card_id in "AA BB CC DD" form

    email = email_number + "@studenti.unimore.it"
    
    # Insert new user:
    try:
        tessere_user = TessereUnimore.objects.get(mail=email)
        
        if tessere_user.id_tessera == card_id:
            if  tessere_user.is_registered == False: # HELP: perchè non registrare solo il fatto che un utente sia registrato?
                tessere_user.is_registered = True
                tessere_user.save()

                # Insert in Django User:
                try:
                    django_user = User.objects.get(username=email_number)
                except (User.DoesNotExist):
                    django_user = User.objects.create(username=email_number, email=email)
                    django_user.set_password(psw)
                    django_user.save()

                    return HttpResponse(template.render({ 'ok': True }, request))
            else:
                return HttpResponse(template.render({ 'already_registered': True }, request))

                
            return HttpResponse(template.render({ 'error': True }, request))

        else:
            print("ERRORE: l'utente è nel DB ma con una tessera diversa!")
            return HttpResponse(template.render({ 'card_id_error': True }, request))

    except (KeyError, TessereUnimore.DoesNotExist):
        return HttpResponse(template.render({ 'error': True }, request))

biblioteche_facolta = { 
    'IngMO' : "ingmo",
    'Matematica' : 'bsi',
    'Fisica' : 'bsi',
    'Medicina' : 'medica',
    'Odontoiatria' : 'medica'
}

def where_to_go(utente):
    biblio = Biblioteche.objects.get(nome = biblioteche_facolta[utente.facolta])
    cap = int((biblio.count / biblio.capienza) * 100)
    if cap < 50:
        return biblio.nome
    else:
        biblio_all = Biblioteche.objects.all()
        for i in biblio_all:
            if i.nome != biblio.nome and (i.count / i.capienza) < (biblio.count / biblio.capienza):
                biblio=i
        return biblio.nome

@login_required
def home(request):
    template = loader.get_template('home.html')
    nome_utente = request.user.username + "@studenti.unimore.it"
    utente = TessereUnimore.objects.get(mail=nome_utente)

    context = {
        'utente' : request.user.username,
        'where_to_go' : where_to_go(utente)
        }

    return HttpResponse(template.render(context, request))

@login_required
def admin_home(request):
    template = loader.get_template('admin.html')

    if request.user.is_superuser:
        context = {
            "superuser":request.user.username
        }
        return HttpResponse(template.render(context, request))

    context = {"superuser":None}
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)
    template = loader.get_template('logout.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def add_student(request):
    template = loader.get_template('add_student.html')
    if request.user.is_superuser:
        try:
            mail = request.POST['mail']
            card_id = request.POST['card_id']
            nome = request.POST['nome']
            cognome = request.POST['cognome']
            facolta = request.POST['facoltà']
            residenza = request.POST['residenza']
            print(card_id)
        except (KeyError):
            context = {
                "superuser":request.user.username,
                "first": True
            }
            return HttpResponse(template.render(context, request))
        if mail is None or nome is None or cognome is None or residenza is None or facolta is None or card_id is None:
            return HttpResponse(template.render({ 'errore': True }, request))
        if len(mail) != 26 or "@studenti.unimore.it" not in mail : #26 is the number of character of all kind of mail
            return HttpResponse(template.render({ 'errore': True }, request))
        if len(nome) > 20 and len(cognome)> 20 and len(residenza)> 30 and len(facolta) > 30:
            return HttpResponse(template.render({ 'errore': True }, request))
        if not checkHEX(card_id) or len(card_id)!=11 :
            return HttpResponse(template.render({ 'errore': True }, request))
        try:
            utente = TessereUnimore.objects.create(mail=mail,id_tessera=card_id,nome=nome,cognome=cognome,facolta=facolta,indirizzo=residenza)
            utente.save()
            context = {
                "superuser":request.user.username,
                "first": True,
                "ok": True
            }
            return HttpResponse(template.render(context, request))
    
        except (KeyError, TessereUnimore.DoesNotExist):
            return HttpResponse(template.render({ 'errore': True }, request))
    
    context = {"superuser":None}
    return HttpResponse(template.render(context, request))

@login_required
def list_student(request):
    template = loader.get_template('list_student.html')

    if request.user.is_superuser:
        context = {
            "superuser":request.user.username
        }
        return HttpResponse(template.render(context, request))

    context = {"superuser":None}
    return HttpResponse(template.render(context, request))

@login_required
def remove_student(request):
    template = loader.get_template('remove_student.html')
    if request.user.is_superuser:
        try:
            mail = request.POST['mail']
            card_id = request.POST['card_id']
        except (KeyError):
            context = {
            "superuser":request.user.username,
            "first": True
            }
            return HttpResponse(template.render(context, request))
        if mail is None or card_id is None:
            print("errore NULL")
            return HttpResponse(template.render({ 'errore': True }, request))
        if len(mail) != 26 or "@studenti.unimore.it" not in mail : #26 is the number of character of all kind of mail
            print("errore mail")
            return HttpResponse(template.render({ 'errore': True }, request))
        if not checkHEX(card_id) or len(card_id)!=11 :
            print("errore card")
            return HttpResponse(template.render({ 'errore': True }, request))
        
        utente = TessereUnimore.objects.get(mail=mail)
        if utente.mail !=mail or utente.id_tessera!=card_id:
            return HttpResponse(template.render({ 'errore': True }, request))
        try:
            utente = TessereUnimore.objects.get(mail=mail)
            user = User.objects.get(username=utente.mail[0:6])
            user.delete()
            utente = TessereUnimore.objects.get(mail=mail)
            utente.delete()
            context = {
                "superuser":request.user.username,
                "first": True,
                "ok": True
            }
            return HttpResponse(template.render(context, request))
    
        except (KeyError, TessereUnimore.DoesNotExist):
            return HttpResponse(template.render({ 'errore': True }, request))
    
    context = {"superuser":None}
    return HttpResponse(template.render(context, request))
