from celery import shared_task
from django.core.management import call_command

@shared_task
def check_appointments():
    call_command('check_appointments')