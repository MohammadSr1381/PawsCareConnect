
from django.urls import path , include
from django.conf.urls.static import static
from PawsCareConnect import settings
from . import views


urlpatterns = [
    path('roleClass/' , views.roleClass , name = 'roleClass'),
    path('registerUser/' , views.registerUser , name = 'registerUser'),
    path('registerClinic/' , views.registerClinic , name = 'registerClinic'),
    path('registerLaboratory/' , views.registerLaboratory , name = 'registerLaboratory'),
    
    path('login/' , views.login , name='login'),
    path('logout/' , views.logout , name='logout'),
    
    
    path('myAccount/', views.myAccount , name='myAccount'),
    
    path('patientDashboard/' , views.patientDashboard , name='patientDashboard'),
    path('clinicDashboard/' , views.clinicDashboard , name='clinicDashboard'),
    path('laboratoryDashboard/' , views.laboratoryDashboard , name='laboratoryDashboard'),
    
    path('activate/<uidb64>/<token>/' , views.activate , name = 'activate'),
    
    path('forgot_password/' , views.forgot_password , name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>' , views.reset_password_validate , name='reset_password_validate'),
    path('reset_password/' , views.reset_password , name='reset_password'),
    
    path('searchClinic/',views.searchClinic , name='searchClinic')


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)