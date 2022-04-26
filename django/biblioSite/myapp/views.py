from datetime import datetime
from django.http import HttpResponse
from django.template import loader


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


#from .models import Product, User, Cart
from django.contrib.auth.decorators import login_required


#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the ecommerce index.")