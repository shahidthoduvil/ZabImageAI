from django.urls import path,include
from .views import *

urlpatterns = [
    path('',generate_image_text,name='name'),
 
]
