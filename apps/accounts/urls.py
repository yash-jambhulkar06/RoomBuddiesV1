from django.urls import path
from .views import  dashboard,login_view,logout_view,register

app_name="accounts"

urlpatterns=[
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
   
]