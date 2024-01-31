# your_app/tasks.py

from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from appointments.models import AppointmentSlot
from clinics.models import ClinicSetting
\
@shared_task
def update_appointment_slots():
    clinics = ClinicSetting.objects.all()

    for clinic_setting in clinics:
        opening_dt = timezone.datetime.combine(timezone.now().date(), clinic_setting.opening_time)
        closing_dt = timezone.datetime.combine(timezone.now().date(), clinic_setting.closing_time)
        current_dt = opening_dt

        while current_dt < closing_dt:
            existing_slot = AppointmentSlot.objects.filter(
                clinic=clinic_setting.clinic,
                date=current_dt.date(),
                start_time=current_dt.time(),
            ).first()

            if not existing_slot:
                slot = AppointmentSlot(
                    clinic=clinic_setting.clinic,
                    date=current_dt.date(),
                    start_time=current_dt.time(),
                    end_time=(current_dt + timedelta(hours=1)).time(),
                )
                slot.save()

            current_dt += timedelta(hours=1)
