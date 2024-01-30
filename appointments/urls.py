from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('create_appointment<int:clinic_id>/<int:slot_id>/', views.create_appointment, name='create_appointment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
