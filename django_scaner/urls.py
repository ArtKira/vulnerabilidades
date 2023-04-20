"""django_scaner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from scanerserver.views import ChangePasswordView
from scanerserver import views#se impprta las vistas desde la app de scaner server 
urlpatterns = [
    #path('admin/', admin.site.urls, name='admin'),#ejemplo de mas vistas 
    path('', views.Login, name='Login'),#Url del login que sera la primera en ver
    # path('', views.scan),#la url lo que se vera en navegador junto con la funcion a ejecutar 
    path('result', views.result),#se crea la vista resultado 
    path('whatweb/', views.whatweb_view, name='whatweb'), # nota la barra diagonal al final
    path('generate_text', views.generate_text),
    path('scan', views.scan, name='scan'),
    path('Logout/', views.Logout, name='Logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('user_registration/', views.user_registration, name='user_registration')#Borrar despues 
]
