from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *


urlpatterns = [
   path('login/',login,name='Login'),
   path('logout/',logout ,name='Login'),
]