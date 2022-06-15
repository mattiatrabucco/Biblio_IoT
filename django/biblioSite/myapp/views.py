#from asyncio.windows_events import NULL
from datetime import datetime, timedelta
import calendar
from tokenize import String
from django.http import HttpResponse
from django.template import loader
import re

from django.contrib import admin

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, get_user_model
from .models import BiblioIngmoCurrent, Biblioteche, LogUnimo, RewardsLog, TessereUnimore
import string
import json

from django.db import connection

from rest_framework import status    
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

def checkHEX(card_id):
    return all(c in string.hexdigits for c in card_id)

def getGiornoEsteso(weekday):
    if weekday == 1:
        return "lunedì"
    if weekday == 2:
        return "martedì"
    if weekday == 3:
        return "mercoledì"
    if weekday == 4:
        return "giovedì"
    if weekday == 5:
        return "venerdì"
    if weekday == 6:
        return "sabato"
    if weekday == 7:
        return "domenica"
    return "N/A"

#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    biblioteche = Biblioteche.objects.all()
    all_bib = {} #oggetto da passare all'HTML
   
    for biblio in biblioteche:
        bib = {}
        if biblio.opening_hours is not None:
            opening_hours = json.loads(biblio.opening_hours)
            open_from = opening_hours[calendar.day_name[datetime.now().weekday()]][0:5] #orario apertura
            try:
                open_from = datetime.strptime(open_from, "%H:%M")
                open_from = open_from.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            except:
                bib["closed"] = True
                bib["opening_hours"] = getGiornoEsteso(datetime.now().isoweekday()) + " chiuso" if opening_hours[calendar.day_name[datetime.now().weekday()]] == "N/A" else "N/A"
                all_bib[biblio.nome] = bib
                continue

            open_until = opening_hours[calendar.day_name[datetime.now().weekday()]][6:]
            open_until = datetime.strptime(open_until, "%H:%M")
            open_until = open_until.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            
            if open_from < datetime.now() < open_until:
                bib["opening_hours"] = opening_hours[calendar.day_name[datetime.now().weekday()]]
                bib["closed"] = False
            else:
                bib["closed"] = True
                bib["opening_hours"] = opening_hours[calendar.day_name[datetime.now().weekday()]]
                all_bib[biblio.nome] = bib
                continue

        else:
            continue
        
        bib["percentage"] = int((biblio.count / biblio.capienza) * 100)
        bib["count"] = biblio.count
        bib["capacity"] = biblio.capienza
        
        if biblio.is_extended:
            bib["extension"] = json.loads(biblio.extension)
            #bib["extension"]["open_until"] = bib["extension"]["open_until"][11:16]
        else:
            bib["extension"] = "N/A"

        all_bib[biblio.nome] = bib
    
    return HttpResponse(template.render({ 'biblioteche' : all_bib }, request))

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

def add_reward_log(utente,biblio_suggestion):
    try :
        reward=RewardsLog.objects.get(id_user=utente.mail[0:6],date=str(datetime.now())[0:10])
        #reward.suggestion=biblio_suggestion
        print("già consigliato")
        #reward.save()
    except (RewardsLog.DoesNotExist):
        reward=RewardsLog.objects.create(id_user=utente.mail[0:6],date=str(datetime.now())[0:10],suggestion=biblio_suggestion)
        print("creato")
        reward.save()

#Checks if a biblio object is open between 1h ahead from now
def biblio_is_open(biblio):
    if biblio.opening_hours is not None:
        opening_hours = json.loads(biblio.opening_hours)
        open_from = opening_hours[calendar.day_name[datetime.now().weekday()]][0:5] #orario apertura
        try:
            open_from = datetime.strptime(open_from, "%H:%M")
            open_from = open_from.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        except:
            #Ho trovato N/A
            return False # ho trovato "N/A"

        open_from -= timedelta(hours=1)
        
        open_until = opening_hours[calendar.day_name[datetime.now().weekday()]][6:]
        open_until = datetime.strptime(open_until, "%H:%M")
        open_until = open_until.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        
        if open_from < datetime.now() < open_until:
            return True
        else:
            #Fuori orario
            return False

def where_to_go(utente):
    biblio = Biblioteche.objects.get(nome = biblioteche_facolta[utente.facolta]) #biblioteca della facoltà dell'utente
    biblio_found = False # booleano per capire se esiste alemeno un biblioteca aperta
    first_biblio = False # booleano per capire se la biblioteca della facoltà dell'utente è aperta
    
    if biblio_is_open(biblio):
        biblio_found = True
        first_biblio = True
        cap = int((biblio.count / biblio.capienza) * 100)
        if cap < 50: #la consigla se sotto al 50%
            add_reward_log(utente,biblio.nome)
            return biblio.nome
    
    biblio_all = Biblioteche.objects.all()
    for i in biblio_all:
        bib = biblio_is_open(i)
        print(bib)
        if bib:
            if (i.nome != biblio.nome and (i.count / i.capienza) < (biblio.count / biblio.capienza)) or first_biblio is False:
                biblio = i #alla fine biblio contiene la biblioteca con percentuale di occupancy minore
                biblio_found = True
                first_biblio = True

    if biblio_found:
        add_reward_log(utente,biblio.nome)
        return biblio.nome
    else:
        return "N/A"

# Ricerca tra i log dell'utente se in data odierna è entrato nella biblio suggerita. Ritorna True o False
def check_eligible_for_reward(utente):
    try:
        reward_logs = RewardsLog.objects.get(id_user = utente.mail[0:6],date=str(datetime.now())[0:10])
        unimo_logs = LogUnimo.objects.filter(id_tessera = utente.id_tessera, mode='IN')
    
    except (LogUnimo.DoesNotExist, RewardsLog.DoesNotExist):
        return False

    for unimo_log in unimo_logs:
        if unimo_log.timestamp[0:10] == str(datetime.now())[0:10]:
            if unimo_log.facolta == reward_logs.suggestion:
                return True
            else:
                return False
    
    return False

# Riscatta il reward se l'utente ne ha diritto. Ritorna "DONE" se riscattato correttamente, "ALREADY" se già riscattato in giornata, "NO" se non ne aveva diritto
def redeem_reward(utente):
    if check_eligible_for_reward(utente):
        if utente.rewards_lastmodified != str(datetime.now())[0:10]:
            utente.rewards_lastmodified = str(datetime.now())[0:10]
            utente.rewards_counter = utente.rewards_counter + 1
            utente.save()
            return "DONE"
        else:
            return "ALREADY"
    else:
        return "NO"

def rewards_level(counter):
    if counter < 1:
        return 0
    elif counter < 5:
        return 1
    elif counter < 10:
        return 2
    elif counter < 50:
        return 3
    else:
        return 4

@login_required
def home(request):
    # if this is a POST request we need to process the form data
    template = loader.get_template('home.html')
    nome_utente = request.user.username + "@studenti.unimore.it"
    try :
        utente = TessereUnimore.objects.get(mail=nome_utente)
    except (TessereUnimore.DoesNotExist):
        return redirect('myapp:index')
    
    dove_andare = where_to_go(utente)

    context = {
        'utente' : utente,
        'where_to_go' : dove_andare,
        'rewards_level': rewards_level(utente.rewards_counter)
    }

    try:
        biblio_gmaps = Biblioteche.objects.get(nome = dove_andare)
        context["gmaps"] = biblio_gmaps.address
        print(biblio_gmaps.address)
    except (Biblioteche.DoesNotExist):
        pass

    if request.method == 'GET':
        return HttpResponse(template.render(context, request))
    else:
        try:
            reward = request.POST['reward']
            if reward == "reward":
                context['reward'] = redeem_reward(utente)

        except (KeyError):
            try:
                telegram_username = request.POST['telegram']
                
                if re.match(r'^[A-Za-z0-9_]+$', telegram_username):
                    utente.telegram_id = telegram_username
                    utente.save()

            except (KeyError):
                return redirect('myapp:home')

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

@csrf_exempt
@api_view(['GET'])
def auth_card(request, facolta, card_id):
    if request.method == "GET":
        if not card_id:
            return Response({'errore': 'non è una card ID'}, status=status.HTTP_404_NOT_FOUND)
        if not isinstance(card_id, str):
            return Response({'errore': 'formato errato'}, status=status.HTTP_404_NOT_FOUND)
        if len(card_id) != 8:
            return Response({'errore': 'lunghezza errata'}, status=status.HTTP_404_NOT_FOUND)
        if not checkHEX(card_id):
            return Response({'errore': 'non una carta valida'}, status=status.HTTP_404_NOT_FOUND)
        
        card_id = ' '.join(card_id[i:i+2] for i in range(0, len(card_id), 2))
        try:
            utente = TessereUnimore.objects.get(id_tessera=card_id)

            if facolta == "ingmo":
                try:
                    log_utente = BiblioIngmoCurrent.objects.get(id_tessera=utente)
                    
                except (BiblioIngmoCurrent.DoesNotExist):
                    return Response({'OK': False}, status=status.HTTP_200_OK)
                
                
                return Response({'OK': True}, status=status.HTTP_200_OK)
            
            return Response({'OK': 'not ingmo'}, status=status.HTTP_200_OK) # TODO: correct
        except (TessereUnimore.DoesNotExist):
            return Response({'errore': 'nessun dato disponibile'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def library(request, biblioteca, card_id):
    if request.method == "POST":
        if not card_id:
            return Response({'errore': 'non è una card ID'}, status=status.HTTP_404_NOT_FOUND)
        if not isinstance(card_id, str):
            return Response({'errore': 'formato errato'}, status=status.HTTP_404_NOT_FOUND)
        if len(card_id) != 8:
            return Response({'errore': 'lunghezza errata'}, status=status.HTTP_404_NOT_FOUND)
        if not checkHEX(card_id):
            return Response({'errore': 'non una carta valida'}, status=status.HTTP_404_NOT_FOUND)
        card_id = ' '.join(card_id[i:i+2] for i in range(0, len(card_id), 2))
        
        if not request.body:
            return Response({'errore': 'non un body valido'}, status=status.HTTP_404_NOT_FOUND)

        body = json.loads(request.body)

        if "way" not in body:
            return Response({'errore': 'non una way valida'}, status=status.HTTP_404_NOT_FOUND)
        
        if body["way"] not in ["IN", "OUT"]:
            return Response({'errore': 'non una way valida'}, status=status.HTTP_404_NOT_FOUND)
        
        if biblioteca == "ingmo":
            #aggiornare count su Biblioteche
            try:
                biblio = Biblioteche.objects.get(nome=biblioteca)

                if body["way"] == "IN": #GOING IN
                    if biblio.count >= biblio.capienza:
                        return Response({'errore': 'nessun dato disponibile'}, status=status.HTTP_404_NOT_FOUND)
                    
                    biblio.count = biblio.count + 1
                    biblio.save()

                    #inserire log su LogUnimo
                    user = TessereUnimore.objects.get(id_tessera=card_id)
                    log = LogUnimo.objects.create(id_tessera=user, timestamp=datetime.now(), mode="IN", facolta=biblioteca)
                    log.save()

                    #aggiungere id su BiblioIngmoCurrent
                    log = BiblioIngmoCurrent.objects.create(id_tessera=user, timestamp=datetime.now())
                    log.save()

                    return Response({'OK': 'entrata corretta'}, status=status.HTTP_200_OK)

                elif body["way"] == "OUT": #GOING OUT
                    if biblio.count > 0:
                        biblio.count = biblio.count - 1
                        biblio.save()
                    
                    #inserire log su LogUnimo
                    user = TessereUnimore.objects.get(id_tessera=card_id)
                    log = LogUnimo.objects.create(id_tessera=user, timestamp=datetime.now(), mode="OUT", facolta=biblioteca)
                    log.save()

                    #rimuovere id su BiblioIngmoCurrent
                    log = BiblioIngmoCurrent.objects.get(id_tessera=user)
                    log.delete()
                    
                    return Response({'OK': 'uscita corretta'}, status=status.HTTP_200_OK)
                    
            except (Biblioteche.DoesNotExist):
                return Response({'errore': 'nessun dato disponibile'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'errore': 'nessun dato disponibile'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
def all_auth_cards(request):
    if request.method == "GET":
        try:
            card_list = list(TessereUnimore.objects.values_list('id_tessera', flat=True))
            
            return Response({'OK': card_list}, status=status.HTTP_200_OK) 

        except (TessereUnimore.DoesNotExist):
            return Response({'errore': 'nessun dato disponibile'}, status=status.HTTP_404_NOT_FOUND)