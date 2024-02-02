from decimal import Decimal, InvalidOperation
from multiprocessing import context
import os
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from site import USER_BASE
from django.shortcuts import redirect, render
from django.urls import reverse
import stripe
from django.conf import settings
from accounts.forms import UserForm, userProfileForm
from accounts.models import Permission, User, UserProfile
from django.contrib import messages , auth
from appointments.models import Appointment
from clinics.models import Clinic, Comment, Rating
from clinics.views import clinicProfile
from patients.models import Patient, Question, Wallet 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash


STRIPE_PUBLIC_KEY='pk_test_51OfMFDCdqFdqb6OvcHnyyuCNEhFvWSQE78LIM3sHn6jxSxpJz3q2XZVt1WVhgtYoij9gU4dNT7Qy90zPtbpZtEZa00LDMDP0iC'
STRIPE_PRIVATE_KEY='sk_test_51OfMFDCdqFdqb6OvAclfrAMaGHjDn4uvkv43J65ittWGebtyzKuh685i8jAiCdnD0LrVDswTQM3nWB29s8N0sgSl00BG36NVtU'


stripe.api_key = STRIPE_PRIVATE_KEY

def pprofile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    prof_instance = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')


        if not (first_name and last_name and phone_number and email):
            messages.error(request, "لطفاً تمامی فیلدها را پر کنید.")
            return redirect('pprofile')

    
        else:
            user_instance.first_name = first_name
            user_instance.last_name = last_name
            user_instance.phone_number = phone_number
            user_instance.email = email
            user_instance.save()
            

            if profile_picture:
                prof_instance.profile_picture = profile_picture
            prof_instance.save()

            messages.success(request, "پروفایل شما با موفقیت آپدیت شد")
            return redirect('pprofile')

    else:
        
        profile_form = userProfileForm(instance=user_instance.userprofile)
        
        #section4
        questions = Question.objects.filter(patient=request.user)
        
        #section3
        patient = get_object_or_404(Patient, user=user_instance)
        wallet = Wallet.objects.get(patient=patient)
        balance = wallet.balance
        wallet_is_activated = wallet.is_activated if wallet else False
        
        
       
        patient_instance = Patient.objects.get(user=user_instance)
        appointments = Appointment.objects.filter(patient=patient_instance , status=False)

        
        
        context = {
            'user': user_instance,
            'profile_form': profile_form,
            'questions': questions,
            'balance' : balance,
            'appointments' : appointments,
            'wallet_is_activated' : wallet_is_activated,
        }
        
        return render(request, 'patients/patientBase.html', context)


@login_required
def askQuestion(request,clinic_id):
    
    clinic = Clinic.objects.get(id=clinic_id)
    context = {
        'clinic' : clinic,
    }
    if request.method == 'POST':
        question_text = request.POST['question_text']
        
        question = Question.objects.create(
            patient=request.user,
            clinic=clinic,
            question_text=question_text
        )
        messages.success(request,'سوال شما ثبت شد')
        return redirect('clinicProfile', clinic_id=clinic.id)
        
    return render(request, 'clinics/clinicProfile.html', context)


@login_required
def viewQuestion(request):
    
    questions = Question.objects.filter(patient=request.user)
    print(1)
    context = {
        'questions': questions,
    }

    return render(request, 'patients/patientBase.html', context)
    



@login_required
def activateWallet(request):
    
    if request.method == 'POST':
        user = request.user
       
        if user.role != User.PATIENT:
            return render(request, '403.html')

        patient = get_object_or_404(Patient, user=user)
        wallet = Wallet.objects.get(patient=patient)

        if not wallet.is_activated:
            wallet.is_activated = True
            wallet.save()
            messages.success(request, 'کیف پول شما با موفقیت فعال شد')
        else:
            messages.success(request, 'کیف پول از قبل فعال است.')

        return redirect('activateWallet')
    
    else:
        user = request.user
        patient = get_object_or_404(Patient, user=user)
        wallet = Wallet.objects.get(patient=patient)  # Define wallet in the else block
        wallet_is_activated = wallet.is_activated if wallet else False
        
        context = {
            'wallet_is_activated' : wallet_is_activated
        }
        
        return render(request, 'patients/patientBase.html', context)

@login_required
def showWalletInfo(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    wallet = wallet = Wallet.objects.get(patient=patient)
    print(f"Wallet Balance: {wallet.balance}")

    context = {
        'wallet' : wallet
    }
    
    return render(request, 'patients/patientBase.html', context)

@require_POST
def increaseBalance(request):

    amount_str = request.POST.get('amount', '0')
    try:
        amount = Decimal(amount_str)
    except InvalidOperation: 
        messages.error(request, 'مبلغ وارد شده معتبر نیست')
        return redirect('pprofile')
    
    user = request.user
    
    if user.role != User.PATIENT:
        return render(request, '403.html')
    
    
    patient = get_object_or_404(Patient, user=user)
    wallet = Wallet.objects.get(patient=patient)
    if not wallet.is_activated:
        return render(request, '403.html')

    amount = float(request.POST.get('amount', 0))

    if 10000 <= amount <= 200000:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',  
                    'product_data': {
                        'name': 'افزایش شارژ',
                    },
                    'unit_amount': int(amount), 
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('pprofile')),
            cancel_url=request.build_absolute_uri(reverse('pprofile')),
        )
        wallet.balance += Decimal(amount)
        wallet.save()
        messages.success(request, f'موجودی با مبلغ {amount} تومان افزایش یافت.')
        return redirect(pprofile)
    else:
        messages.error(request, 'مبلغ می‌تواند بین 10 هزار تا 200 هزار تومان باشد')
        return redirect(pprofile)


@login_required
def changePassword(request):
    
    user_instance = User.objects.get(id=request.user.id)
    patient_instance = Patient.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if not current_password or not new_password1 or not new_password2:
            messages.error(request, 'لطفاً تمامی فیلدها را پر کنید')
        elif not user_instance.check_password(current_password):
            messages.error(request, 'رمز شما اشتباه است')
        elif new_password1 != new_password2:
            messages.error(request, 'رمز جدید و تکرار آن باهم مطابقت ندارد')
        else:
            try:
                validate_password(new_password1, user=user_instance)
            except ValidationError as e:
                messages.error(request , 'رمز عبور تعریف شده شما ساده تر از استاندارد است')
                return render(request, 'patients/patientBase.html') 
            user_instance.set_password(new_password1)
            user_instance.save()
            update_session_auth_hash(request, user_instance)
            messages.success(request, 'رمز شما با موفقیت تغییر یافت')
    
    return redirect(pprofile)

@login_required
def deletePatientProfile(request):

    user_instance = User.objects.get(id=request.user.id)
    patient_instance = Patient.objects.get(user=request.user)
    
    if request.method == "POST":
        user_instance.delete()
        patient_instance.delete()
        auth.logout(request) 
        messages.info(request, 'You are logged out.')
        return redirect('home')
    else :
        return render(request, 'patients/patientBase.html')
    
@login_required    
def putComment(request , clinic_id):
    permission = Permission.objects.get(name='permission')
    user_instance = User.objects.get(id=request.user.id)
    print(user_instance.role)
    if user_instance.role != 1 or permission.clinicComment:
        messages.error(request , 'کلینیک ها نمیتوانند راجع به یکدیگر نظر بدهند')
        return redirect(clinicProfile , clinic_id=clinic_id)  
  
    patient_instance = Patient.objects.get(user=request.user)
    clinic = Clinic.objects.get(id=clinic_id)
    
    existing_comment = Comment.objects.filter(patient=user_instance, clinic=clinic).exists()

    if existing_comment:
        messages.error(request, 'شما قبلاً نظر داده‌اید.')
        return redirect(clinicProfile, clinic_id=clinic_id)
    
    else :
        if (permission.patientComment != False):
            messages.error(request,'فعلا امکان کامنت دهی بسته شده است')
            return redirect(clinicProfile , clinic_id=clinic_id)
        if request.method == 'POST' :
            comment_text = request.POST.get('comment_text')
            if comment_text:

                comment = Comment.objects.create(
                patient=user_instance,
                clinic=clinic,
                comment_text=comment_text
                )
                messages.success(request,'نظر شما اضافه شد')
                return redirect(clinicProfile , clinic_id=clinic_id)

            else : 
                messages.error(request,'کامنت باید پر شود')
                return redirect(clinicProfile , clinic_id=clinic_id)

        context = {
            'comment' : comment
        }
        return render(request, 'clinics/clinicProfile.html', context)
    
@login_required    
def putRating(request , clinic_id):
    permission = Permission.objects.get(name='permission')
    user_instance = User.objects.get(id=request.user.id)
    
    print(user_instance.role)
    if user_instance.role != 1 or permission.clinicRating:
        messages.error(request , 'کلینیک ها نمیتوانند به هم امتیاز دهند')
        return redirect(clinicProfile , clinic_id=clinic_id)
    
    patient_instance = Patient.objects.get(user=request.user)
    clinic = Clinic.objects.get(id=clinic_id)
    
    existing_rating = Rating.objects.filter(patient=user_instance, clinic=clinic).exists()

    if existing_rating:
        messages.error(request, 'شما قبلاً امتیاز داده‌اید.')
        return redirect(clinicProfile, clinic_id=clinic_id)
    


    else :
        if (permission.patientRating !=False) :
            messages.error(request,'فعلا امکان امتیاز دهی بسته شده است')
            return redirect(clinicProfile , clinic_id=clinic_id)
        if request.method == 'POST' :
            score = request.POST.get('score')
            if score:

                rating = Rating.objects.create(
                patient=user_instance,
                clinic=clinic,
                score=score
                )
                messages.success(request,'امتیاز شما اضافه شد')
                return redirect(clinicProfile , clinic_id=clinic_id)

            else : 
                messages.error(request,'امتیاز نباید خالی باشد')
                return redirect(clinicProfile , clinic_id=clinic_id)

        context = {
            'rating' : rating
        }
        return render(request, 'clinics/clinicProfile.html', context)

from django.core.mail import EmailMessage

@login_required    
def deleteAppointmentsPatient(request,appointment_id):
    
    try:
        user_instance = request.user 
        patient_instance = Patient.objects.get(user=user_instance)
        
        appointment_instance = Appointment.objects.get(id=appointment_id)
        appointment_instance.delete()
        
        from_email = settings.DEFAULT_FROM_EMAIL
        clinic_email = appointment_instance.clinic.user.email
        subject = 'حذف نوبت'
        message = f'کاربر نوبت خود با شما در تایم {appointment_instance.appointment_datetime} را حذف کرده است'
        mail = EmailMessage(subject , message , to=[clinic_email])
        mail.send()
        messages.success(request , 'نوبت با موفقیت لغو شد')
    except :
        messages.error(request , 'قادر به انجام عملیات مورد نظر شما نمی باشیم لطفا بعدا تلاش کنید')


    return redirect(pprofile)

    
    






            
    
