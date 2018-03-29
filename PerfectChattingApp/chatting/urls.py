# Author : Mr King
# Date : 2018-03-16 17:05 


from django.urls import path
from . import views

urlpatterns = [
    path(r'add_contact/', views.Contact.as_view()),
    path(r'send_msg/', views.SendMsg.as_view()),
]


