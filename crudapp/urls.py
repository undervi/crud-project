"""crudProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from crudapp.views import create, read, update, delete, date_desc, date_asc, title_asc, writer_asc, img_check

app_name = "crudapp"

urlpatterns = [
    path('', date_desc, name='home'),
    path('date_desc/', date_desc, name='home'),
    path('date_asc/', date_asc, name='date_asc'),
    path('title_asc/', title_asc, name='title_asc'),
    path('writer_asc/', writer_asc, name='writer_asc'),
    path('create/', create, name='create'),
    path('read/', read, name='read'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete'),
]
