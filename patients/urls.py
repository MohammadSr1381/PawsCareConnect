from os import name
from django.urls import path , include
from django.conf.urls.static import static
from PawsCareConnect import settings
from . import views


urlpatterns = [
    path('pprofile/' , views.pprofile , name = 'pprofile'),
    path('askQuestion/<clinic_id>' , views.askQuestion , name = 'askQuestion'),
    path('activateWallet/' , views.activateWallet , name = 'activateWallet'),
    path('increaseBalance/' , views.increaseBalance , name = 'increaseBalance'),
    path('showWalletInfo/' , views.showWalletInfo , name = 'showWalletInfo'),
    path('deletePatientProfile/' , views.deletePatientProfile , name = 'deletePatientProfile'),
    path('changePassword/' , views.changePassword , name = 'changePassword'),
    path('viewQuestion/' , views.viewQuestion , name='viewQuestion'),
    path('putComment/<int:clinic_id>/' , views.putComment  ,name='putComment'),
    path('putRating/<int:clinic_id>/' , views.putRating  ,name='putRating'),
    path('deleteAppointmentsPatient/<int:appointment_id>' , views.deleteAppointmentsPatient , name='deleteAppointmentsPatient'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)