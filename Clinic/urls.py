from django.urls import path
from .views import *
from .views import sms_reply

urlpatterns = [
    path('', HeroView, name='hero'),
    path('sms/', sms_reply, name='sms_reply'),

]

