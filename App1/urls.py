from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('cregister',views.cregister),
    path('login',views.login),
    path('clogin',views.clogin),
    path('lsignup',views.lsignup),
    path('csignup',views.csignup),
    path('lsignin',views.lsignin),
    path('labourpage',views.labourpage),
    path('csignin',views.csignin),
    path('companypage',views.companypage),
    path('jobboard',views.jobboard),
    path('position',views.position),
    path('addposition',views.addposition),
    path('apply/<int:position_id>',views.apply),
    path('view/<int:position_id>',views.view),
    ]
