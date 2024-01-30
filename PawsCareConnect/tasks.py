# tasks.py
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from appointments.models import Appointment


@shared_task
def delete_old_appointments():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    Appointment.objects.filter(appointment_datetime__lt=one_hour_ago).delete()
