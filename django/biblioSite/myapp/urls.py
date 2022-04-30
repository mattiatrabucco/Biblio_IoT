from django.urls import path


from . import views


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
]
