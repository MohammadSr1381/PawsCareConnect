from django.urls import path , include
from django.conf.urls.static import static
from PawsCareConnect import settings
from . import views


urlpatterns = [
    path('pprofile/' , views.pprofile , name = 'pprofile'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)