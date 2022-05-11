from django.contrib import admin

from .models import TessereUnimore, Biblioteche
# Register your models here.

class TessereUnimoreAdmin(admin.ModelAdmin):
    list_display = ('id_tessera', 'nome', 'cognome', 'facolta', 'mail')

class BibliotecheAdmin(admin.ModelAdmin):
    list_display = ('nome', 'count', 'capienza', 'is_extended', 'extension')

admin.site.register(TessereUnimore, TessereUnimoreAdmin)
admin.site.register(Biblioteche, BibliotecheAdmin)