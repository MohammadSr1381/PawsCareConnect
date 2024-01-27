from django.urls import path , include
from django.conf.urls.static import static
from PawsCareConnect import settings
from . import views


urlpatterns = [
    path('cprofile/' , views.cprofile , name = 'cprofile'),
    path('lprofile/' , views.lprofile , name = 'lprofile'),
    path('answerQuestion/<int:clinic_id>' , views.answerQuestion , name = 'answerQuestion'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)