from django import forms
from clinics.models import Clinic



class ClinicForm(forms.ModelForm):
    class Meta :
        model = Clinic 
        fields = ['clinic_name' , 'clinic_license' , 'citizen_id' , 'city' , 'address']