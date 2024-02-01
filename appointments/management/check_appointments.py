from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from appointments.models import Appointment


class Command(BaseCommand):
    help = 'با سلام شما امروز نوبت دارید'

    def handle(self, *args, **options):
        today_local = datetime.now().date()
        start_of_day = datetime.combine(today_local, datetime.min.time())
        end_of_day = datetime.combine(today_local, datetime.max.time())
        appointments_today = Appointment.objects.filter(  appointment_datetime__range=(start_of_day, end_of_day))

        for appointment in appointments_today:
            self.send_appointment_email(appointment)

    def send_appointment_email(self, appointment):
        # Customize the email sending logic here
        subject = 'یادآوری'
        message = f'سلام {appointment.patient.user.first_name},\n\nشما امروز نوبتی دارید {appointment.appointment_datetime}.\n\nبا تشکر از نوبت دهی'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [appointment.patient.user.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)
