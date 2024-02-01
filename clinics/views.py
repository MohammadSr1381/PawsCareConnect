from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Avg

from dbm import error
from multiprocessing import context
from site import USER_BASE

from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserForm, userProfileForm
from accounts.models import User, UserProfile
from appointments.models import Appointment, AppointmentSlot

from clinics.forms import AnswerForm, CRUDClinicForm, CRUDUserForm, CRUDUserProfileForm, ClinicForm
from clinics.models import Clinic, ClinicSetting, Comment, Rating
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
from patients.models import Patient, Question, Wallet 
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from django.utils import timezone

def cprofile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    clinic_instance = Clinic.objects.get(user=request.user)
    prof_instance = UserProfile.objects.get(user=request.user)
    
    if request.method == "POST":
       
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        citizen_id = request.POST.get('citizen_id')
        city = request.POST.get('city')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')


        if not (first_name and last_name and phone_number and email and citizen_id and city and address):
            messages.error(request, "لطفاً تمامی فیلدها را پر کنید.")
            return redirect('cprofile')
        
        else:
            user_instance.first_name = first_name
            user_instance.last_name = last_name
            user_instance.phone_number = phone_number
            user_instance.email = email
            user_instance.save()

            if profile_picture:
                prof_instance.profile_picture = profile_picture
                prof_instance.save()

            clinic_instance.citizen_id = citizen_id
            clinic_instance.city = city
            clinic_instance.address = address
            clinic_instance.save()

            messages.success(request, "پروفایل شما با موفقیت آپدیت شد")
            return redirect('cprofile')

    else:
        user_instance = User.objects.get(id=request.user.id)
        clinic = Clinic.objects.get(user=user_instance)
        questions = Question.objects.filter(clinic=clinic)
        profile_form = userProfileForm(instance=user_instance.userprofile)
        clinic_form = ClinicForm(instance=clinic_instance)
        clinicSetting = ClinicSetting.objects.get(clinic=clinic)
        
        

  
        clinic_instance = Clinic.objects.get(user=user_instance)
        appointments = Appointment.objects.filter(clinic=clinic_instance , status=False)
        slots =AppointmentSlot.objects.filter(clinic=clinic)
        for appointment in appointments :
            print(appointment.appointment_datetime)


        today_local = datetime.now().date()

        start_of_day = datetime.combine(today_local, datetime.min.time())
        end_of_day = datetime.combine(today_local, datetime.max.time())
        print(start_of_day)
        # Filter appointments for the local date (ignoring time)
        today_appointments = Appointment.objects.filter(
            appointment_datetime__range=(start_of_day, end_of_day)
        )
  
        print("Clinic:", clinic)
        print("Appointments:", today_appointments)
        context = {
            'user': user_instance,
            'today_appointments': today_appointments,
            'profile_form': profile_form,
            'clinic_form': clinic_form,
            'location_choices': clinic_instance.LOCATION_CHOICE ,
            'clinic': clinic, 
            'questions': questions,
            'appointments' : appointments,
            'clinicSetting' : clinicSetting,
            'slots' : slots,
        }
        return render(request, 'clinics/clinicDashboard.html', context)

@login_required
def deleteClinicProfile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    clinic_instance = Clinic.objects.get(user=request.user)
    
    if request.method == "POST":
        user_instance.delete()
        clinic_instance.delete()
        auth.logout(request) 
        messages.info(request, 'You are logged out.')
        return redirect('home')
    else :
        return render(request, 'clinics/clinicDashboard.html')
    

@login_required
def changeClinicPassword(request):
    
    user_instance = User.objects.get(id=request.user.id)
    clinic_instance = Clinic.objects.get(user=request.user)
    
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
            user_instance.set_password(new_password1)
            user_instance.save()
            update_session_auth_hash(request, user_instance)
            messages.success(request, 'رمز شما با موفقیت تغییر یافت')
    
    return redirect(cprofile)
        
    
    
def lprofile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    clinic_instance = Clinic.objects.get(user=request.user)
    prof_instance = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        citizen_id = request.POST.get('citizen_id')
        city = request.POST.get('city')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')


        if not (first_name and last_name and phone_number and email and citizen_id and city and address):
            messages.error(request, "لطفاً تمامی فیلدها را پر کنید.")
            return redirect('cprofile')

    
        else:
            user_instance.first_name = first_name
            user_instance.last_name = last_name
            user_instance.phone_number = phone_number
            user_instance.email = email
            user_instance.save()

            if profile_picture:
                prof_instance.profile_picture = profile_picture
                prof_instance.save()

            clinic_instance.citizen_id = citizen_id
            clinic_instance.city = city
            clinic_instance.address = address
            clinic_instance.save()

            messages.success(request, "پروفایل شما با موفقیت آپدیت شد")
            return redirect('cprofile')

    else:
        profile_form = userProfileForm(instance=user_instance.userprofile)
        clinic_form = ClinicForm(instance=clinic_instance)
        context = {
            'user': user_instance,
            'profile_form': profile_form,
            'clinic_form': clinic_form,
            'location_choices': clinic_instance.LOCATION_CHOICE 
        }
        return render(request, 'clinics/clinicDashboard.html', context)
    

@login_required
def answerQuestion(request):
    user_instance = User.objects.get(id=request.user.id)
    clinic = Clinic.objects.get(user=user_instance)
    questions = Question.objects.filter(clinic=clinic)
    
    if request.method == 'POST':
        question_id = request.POST.get('id')
        answer_form = request.POST.get('answer_field')
        question = get_object_or_404(Question, id=question_id, clinic=clinic)

        if answer_form:
            question.answer_text = answer_form
            question.is_answered = True
            question.save()

            messages.success(request,"جواب شما با موفقیت ثبت شد")
            return redirect(cprofile)
            
        else:
            messages.error(request, "لطفاً جواب را وارد کنید.")
            return redirect('cprofile')
        
    else :
        user_instance = User.objects.get(id=request.user.id)
        clinic = Clinic.objects.get(user=user_instance)
        questions = Question.objects.filter(clinic=clinic)
        context = {'clinic': clinic, 'questions': questions}
        return render(request, 'clinics/clinicDashboard.html', context)



def clinicProfile(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    clinicSetting = ClinicSetting.objects.get(clinic=clinic)
    comments = Comment.objects.filter(clinic=clinic)
    
    score_avg = Rating.objects.filter(clinic=clinic).aggregate(Avg('score'))['score__avg']
    
    context = {
        'clinic': clinic,
        'clinicSetting': clinicSetting,
        'comments': comments,
        'ratingAvg': score_avg,
    }
    return render(request, 'clinics/clinicProfile.html', context)

@login_required
def updateSettings(request):
    
    user_instance = User.objects.get(id=request.user.id)
    clinic_instance = Clinic.objects.get(user=request.user)
    clinic_setting = ClinicSetting.objects.get(clinic=clinic_instance)
    
    if request.method == "POST":
       
        description = request.POST.get("description")
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        price = request.POST.get('price')
        
        if not(description and opening_time and closing_time and price):
            messages.error(request, "لطفاً تمامی فیلدها را پر کنید.")
            return redirect('cprofile')
        
        else:
            clinic_setting.description = description
            clinic_setting.opening_time = opening_time
            clinic_setting.closing_time = closing_time
            clinic_setting.cost = price
            clinic_setting.save()
            
        opening_dt = datetime.strptime(opening_time, '%H:%M')
        closing_dt = datetime.strptime(closing_time, '%H:%M')
        current_dt = opening_dt

        while current_dt < closing_dt:
            existing_slot = AppointmentSlot.objects.filter(
                clinic=clinic_instance,
                date=current_dt.date(),
                start_time=current_dt.time(),
            ).first()

            if not existing_slot:
                slot = AppointmentSlot(
                    clinic=clinic_instance,
                    date=current_dt.date(),
                    start_time=current_dt.time(),
                    end_time=(current_dt + timedelta(hours=1)).time(),
                )
                slot.save()

            current_dt += timedelta(hours=1)

        messages.success(request, "تنظیمات شما با موفقیت آپدیت شد")
        return redirect('cprofile')
        
    return render(request, 'clinics/clinicDashboard.html')



from django.core.mail import EmailMessage

@login_required    
def deleteAppointmentsClinic(request,appointment_id):
    try:
        user_instance = request.user 
        clinic_instance = Clinic.objects.get(user=user_instance)
        wallet_instance = Wallet.objects.get(patient=user_instance.patient)
        appointment_instance = Appointment.objects.get(id=appointment_id)
        appointment_instance.delete()
        wallet_instance.balance += appointment_instance.cost
        wallet_instance.save()
        from_email = settings.DEFAULT_FROM_EMAIL
        patient_email = appointment_instance.patient.user.email
        subject = 'حذف نوبت'
        message = f'کلینیک {{appointment_instance.clinic.clinic_name}} نوبت خود با شما در تایم {appointment_instance.appointment_datetime} را حذف کرده است'
        mail = EmailMessage(subject , message , to=[patient_email])
        mail.send()
        
        messages.success(request , 'نوبت با موفقیت لغو شد')
    except :
        messages.error(request , 'قادر به انجام عملیات مورد نظر شما نمی باشیم لطفا بعدا تلاش کنید')

    return redirect(cprofile)
