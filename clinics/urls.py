from django.urls import path , include
from django.conf.urls.static import static
from PawsCareConnect import settings
from . import views


urlpatterns = [
    path('cprofile/' , views.cprofile , name = 'cprofile'),
    path('lprofile/' , views.lprofile , name = 'lprofile'),
    path('updateSettings/' , views.updateSettings , name = 'updateSettings'),
    path('answerQuestion/' , views.answerQuestion , name = 'answerQuestion'),
    path('deleteClinicProfile/' , views.deleteClinicProfile , name = 'deleteClinicProfile'),
    path('changeClinicPassword/' , views.changeClinicPassword , name = 'changeClinicPassword'),
    path('clinicProfile/<int:clinic_id>/', views.clinicProfile, name='clinicProfile'),
    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)