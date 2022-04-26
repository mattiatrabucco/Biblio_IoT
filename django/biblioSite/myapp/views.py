from datetime import datetime
from django.http import HttpResponse
from django.template import loader


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.contrib.auth.decorators import login_required


#path('', views.index, name='index')
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the ecommerce index.")

@login_required
def home(request):
    #product_list = Product.objects.all().order_by('name') #.get(pk=post_id) .order_by('-pub_date')[:5]
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))