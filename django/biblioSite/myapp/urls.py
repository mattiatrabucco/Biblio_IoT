from sys import api_version
from django.urls import path


from . import views

api_path="api/v1/"
app_name='myapp'
urlpatterns = [
    path('',views.index, name='index'),
    path('home/',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('add_student/', views.add_student, name='add_student'),
    path('remove_student/', views.remove_student, name='remove_student'),
    path('list_student/', views.list_student, name='list_student'),

    path(api_path + "all_auth_cards/", views.all_auth_cards, name='auth_card'),
    path(api_path + "auth_card/<str:facolta>/<str:card_id>/", views.auth_card, name='auth_card'),
    path(api_path + "library/<str:biblioteca>/<str:card_id>/", views.library, name='library'),
]
