from django.db import models
from accounts.models import User, UserProfile
from clinics.models import Clinic

class Patient(models.Model):
    user = models.OneToOneField(User, related_name='patient_user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='patient_profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class Wallet(models.Model):
    patient = models.OneToOneField(Patient, related_name='wallet', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_activated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient.user.first_name

class Question(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asked_questions')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='answered_questions')
    question_text = models.TextField(blank=False)
    answer_text = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question from {self.patient.email} to {self.clinic.clinic_name}"
