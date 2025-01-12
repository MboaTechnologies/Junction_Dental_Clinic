from django.urls import path
from .views import *

urlpatterns = [
    path('', HeroView, name='hero'),

]
