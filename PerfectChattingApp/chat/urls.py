# Author : Mr King
# Date : 2018-03-11 20:38 


from django.urls import path
from . import views

urlpatterns = [
    path(r'home/', views.Home.as_view()),
    path(r'login/', views.Login.as_view()),
    path(r'register/', views.Register.as_view()),
    path(r'email/', views.EmailCode.as_view()),
    path(r'img_file.html/', views.SendHeadImg.as_view()),
    path(r"history_img.html/", views.HistoryImg.as_view()),
    path(r'homelogin/', views.LoginHome.as_view()),
]

