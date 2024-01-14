from base64 import urlsafe_b64decode
import email
from email import message
from os import error
import re
from django.shortcuts import render , redirect
from django.http import HttpResponse
from accounts.utils import detectUser, send_verification_email

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from clinics.forms import ClinicForm
from clinics.models import Clinic
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied


def check_role_patient(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
    
    
def check_role_patient(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
    
def check_role_clinic(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied
    
def check_role_Laboratory(user):
    if user.role ==3:
        return True
    else:
        raise PermissionDenied

def roleClass(request):
    return render(request , 'accounts/roleClass.html')

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'u r already logged in')
        return redirect('dashboard')
    elif request.method == "POST" :
        
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
            
            #verify
            mail_subject = 'لطفا اکانت خود را فعال کنید'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            
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
    if request.user.is_authenticated:
        messages.warning(request,'u r already logged in')
        return redirect('dashboard')
    elif request.method == "POST" :
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
            
            #verify
            mail_subject = 'لطفا اکانت خود را فعال کنید'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)   
                     
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
    if request.user.is_authenticated:
        messages.warning(request,'u r already logged in')
        return redirect('dashboard')
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
            
            #verify
            mail_subject = 'لطفا اکانت خود را فعال کنید'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            
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

def activate(request , uidb64 , token):

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request,'congrats ur account is activate')
        return redirect('myAccount')
    else:
        
        print(default_token_generator.check_token(user , token))
        print('hello')
        messages.error(request , 'invalid activation link :')
        return redirect('myAccount')
        
    


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'u r already logged in')
        return redirect('dashboard')
    elif request.method =='POST':   
        email = request.POST["email"]
        password = request.POST["password"]
    
        user = auth.authenticate(email=email , password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'u r logged in')
            return redirect('myAccount')
        else :
            messages.error(request , 'invalid login credentials')
            return redirect('login')
        
    return render(request , 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'u r logged out')
    return redirect('home')

@login_required(login_url ='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url ='login')
@user_passes_test(check_role_patient)
def patientDashboard(request):
    return render(request, 'accounts/patientDashboard.html')

@login_required(login_url ='login')
@user_passes_test(check_role_clinic)
def clinicDashboard(request):
    return render(request, 'accounts/clinicDashboard.html')

@login_required(login_url ='login')
@user_passes_test(check_role_Laboratory)
def laboratoryDashboard(request):
    return render(request, 'accounts/laboratoryDashboard.html') 


def forgot_password(request):
    
    if request.method == 'POST':
        
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            #send password reset email
            mail_subject = 'تغییر رمز عبور' 
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            
            messages.success(request ,'password reset link has been sent to ur email')
            return redirect('login')
        else :
            messages.success(request , 'account does not exist')
            return redirect('forgot_password')
        
    return render (request , 'accounts/forgot_password.html')


def reset_password_validate(request , uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user , token):
            request.session['uid'] = uid
            messages.info(request , 'please reset your password')
            return redirect('reset_password')
    else:
        messages.error(request , 'this link has expired')
        return redirect('myAccount')
    

def reset_password(request):
    
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            
            if password == confirm_password:
                pk = request.session.get('uid')
                user = User.objects.get(pk=pk)
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request , 'password changed successfully')
                return redirect('login')
            else:
                messages.error('passwords do not match')
                return redirect('reset_password')
            
            
        return render (request , 'accounts/reset_password.html')

