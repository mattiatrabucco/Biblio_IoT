from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def logout_view(request):
    #Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('')