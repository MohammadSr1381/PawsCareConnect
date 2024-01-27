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
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)