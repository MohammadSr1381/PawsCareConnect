from django.urls import path , include
from . import views


urlpatterns = [
    path('roleClass/' , views.roleClass , name = 'roleClass'),
    path('registerUser/' , views.registerUser , name = 'registerUser'),
    path('registerClinic/' , views.registerClinic , name = 'registerClinic'),
    path('registerLaboratory/' , views.registerLaboratory , name = 'registerLaboratory'),
    
    path('login/' , views.login , name='login'),
    path('logout/' , views.logout , name='logout'),
    path('mtAccount/', views.myAccount , name='myAccount'),
    path('patientDashboard/' , views.patientDashboard , name='patientDashboard'),
    path('clinicDashboard/' , views.clinicDashboard , name='clinicDashboard'),
    path('laboratoryDashboard/' , views.laboratoryDashboard , name='laboratoryDashboard'),
]