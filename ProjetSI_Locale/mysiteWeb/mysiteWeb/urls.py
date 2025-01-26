"""
URL configuration for mysiteWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from App1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('App1/', views.index, name='index'),
    path('suppression/', views.suppression, name='suppression'),
    path('calendar/', views.calendrier, name='calendar'),
    path('admini/', views.admini, name='admini'),
    path('reservation/', views.reservation, name='reservation'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('box/', views.box, name='box'),
    path('creation/', views.creation, name='creation'),
    path('move_to_blacklist/', views.move_to_blacklist, name='move_to_blacklist'),
    path('move_to_whitelist/', views.move_to_whitelist, name='move_to_whitelist'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('logout/', views.logout_view, name='logout'),

    
]
