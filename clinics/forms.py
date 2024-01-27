from pyexpat import model
from attr import fields
from django import forms
from accounts.models import User, UserProfile
from clinics.models import Clinic
from patients.models import Question



class ClinicForm(forms.ModelForm):
    class Meta :
        model = Clinic 
        fields = ['clinic_name' , 'clinic_license' , 'citizen_id' , 'city' , 'address']


class AnswerForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Question
        fields = ['id', 'answer_text']
   
        
from django import forms
from accounts.forms import UserForm , userProfileForm 

class CRUDClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic 
        fields = ['city', 'citizen_id']

class CRUDUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'phone_number' , 'email']

class CRUDUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['profile_picture']
