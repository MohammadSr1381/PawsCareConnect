from datetime import datetime, timedelta
from email.policy import default
from django.db import models
from clinics.models import Clinic
from patients.models import Patient


class Appointment(models.Model):
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patientAppointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinicAppointments')
    appointment_datetime = models.DateTimeField()
    status = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class AppointmentSlot(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='appointment_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)  # Add this line

    def __str__(self):
        return f"{self.clinic.clinic_name} - {self.date} {self.start_time}-{self.end_time}"



    def generate_appointment_slots(clinic, start_date=None, end_date=None):
        # If start_date is not provided, start generating slots from tomorrow
        if start_date is None:
            start_date = datetime.now().date() + timedelta(days=1)

        # If end_date is not provided, generate slots for a week (7 days)
        if end_date is None:
            end_date = start_date + timedelta(days=7)

        current_date = start_date

        while current_date <= end_date:
            start_time = clinic.clinic_setting.opening_time
            end_time = clinic.clinic_setting.closing_time

            while start_time < end_time:
                slot = AppointmentSlot(
                    clinic=clinic,
                    date=current_date,
                    start_time=start_time,
                    end_time=start_time + timedelta(hours=1)
                )
                slot.save()

                start_time += timedelta(hours=1)

            current_date += timedelta(days=1)
