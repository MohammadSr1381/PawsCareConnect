from django.shortcuts import render , redirect
from django.http import HttpResponse

from clinics.forms import ClinicForm
from clinics.models import Clinic
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages


def roleClass(request):
    return render(request , 'accounts/roleClass.html')

def registerUser(request):
    if request.method == "POST" :
        
        form = UserForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name , last_name = last_name , phone_number = phone_number , email = email, password = password)
            user.role = User.PATIENT    
            user.save()
            messages.success(request , "your account has been saved successfully")
            print('user created successfully')
            return redirect('registerUser')
        else :
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request , 'accounts/registerUser.html' , context)



def registerClinic(request):
    if request.method == "POST" :
        form = UserForm(request.POST)
        clinic_form = ClinicForm(request.POST , request.FILES)
        if form.is_valid() and clinic_form.is_valid():
                     
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            clinic_name = clinic_form.cleaned_data['clinic_name']
            clinic_license = clinic_form.cleaned_data['clinic_license']
            citizen_id = clinic_form.cleaned_data['citizen_id']
            city = clinic_form.cleaned_data['city']
            address = clinic_form.cleaned_data['address']
            
            user = User.objects.create_user(first_name = first_name , last_name = last_name , phone_number = phone_number , email = email, password = password)
            user.role = User.CLINIC  
            user.save()
            
            user_profile = UserProfile.objects.get(user = user)
            user_profile.citizen_id = citizen_id
            user_profile.city = city
            user_profile.save()
            
            clinic = Clinic(user = user , user_profile = user_profile , clinic_name = clinic_name , citizen_id = citizen_id , city = city , address = address , clinic_license = clinic_license)
            clinic.save()
            messages.success(request , "your account made successfully")
            return redirect('registerClinic')
            
        else :
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
        clinic_form = ClinicForm()
    
    context = {
        'form' : form ,
        'clinic_form' : clinic_form ,
    }
    return render(request , 'accounts/registerClinic.html' ,context)



def registerLaboratory(request):
    if request.method == "POST" :
        form = UserForm(request.POST)
        clinic_form = ClinicForm(request.POST , request.FILES)
        if form.is_valid() and clinic_form.is_valid():
                     
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            clinic_name = clinic_form.cleaned_data['clinic_name']
            clinic_license = clinic_form.cleaned_data['clinic_license']
            citizen_id = clinic_form.cleaned_data['citizen_id']
            city = clinic_form.cleaned_data['city']
            address = clinic_form.cleaned_data['address']
            
            user = User.objects.create_user(first_name = first_name , last_name = last_name , phone_number = phone_number , email = email, password = password)
            user.role = User.LABORATORY 
            user.save()
            
            user_profile = UserProfile.objects.get(user = user)
            user_profile.citizen_id = citizen_id
            user_profile.city = city
            user_profile.save()
            
            clinic = Clinic(user = user , user_profile = user_profile , clinic_name = clinic_name , citizen_id = citizen_id , city = city , address = address , clinic_license = clinic_license)
            clinic.save()
            messages.success(request , "your account made successfully")
            return redirect('registerClinic')
            
        else :
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
        clinic_form = ClinicForm()
    
    context = {
        'form' : form ,
        'clinic_form' : clinic_form ,
    }
    return render(request , 'accounts/registerLaboratory.html' ,context)