
from email.message import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def cancel_by_patient(request , reciever ,  mail_subject , email_template , x):
    
    from_email = settings.DEFAULT_FROM_EMAIL
    message = f'کاربر نوبت خود با شما در تایم {appointment.appointment_datetime} را حذف کرده است'
    to_email = reciever
    mail = EmailMessage(mail_subject , message , to=[to_email])
    mail.send()
    
