from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages , auth
import stripe
from clinics.views import clinicProfile
from .models import Appointment, AppointmentSlot, Clinic , Patient, PaymentIntent
from django.contrib.auth.decorators import login_required
from accounts.models import Permission

STRIPE_PUBLIC_KEY='pk_test_51OfMFDCdqFdqb6OvcHnyyuCNEhFvWSQE78LIM3sHn6jxSxpJz3q2XZVt1WVhgtYoij9gU4dNT7Qy90zPtbpZtEZa00LDMDP0iC'
STRIPE_PRIVATE_KEY='sk_test_51OfMFDCdqFdqb6OvAclfrAMaGHjDn4uvkv43J65ittWGebtyzKuh685i8jAiCdnD0LrVDswTQM3nWB29s8N0sgSl00BG36NVtU'



@login_required
def create_appointment(request, clinic_id, slot_id):
    permission = Permission.objects.get(name='permission')

    if request.user.role != 1 or permission.clinicAppointment:
        messages.error(request , 'کلینیک ها نمیتوانند از همدیگر نوبت بگیرند')
        return redirect(clinicProfile , clinic_id=clinic_id)
    slot = AppointmentSlot.objects.get(id=slot_id)


    opening_hour = slot.start_time
    today_date = datetime.now().date()
    appointment_datetime = datetime.combine(today_date, opening_hour)
    
    if slot.is_available:
        clinic = Clinic.objects.get(id=clinic_id)
        patient = Patient.objects.get(user=request.user)
        
        if (permission.patientAppointment !=False) :
            messages.error(request,'فعلا امکان نوبت دهی بسته شده است')
            return redirect(clinicProfile , clinic_id=clinic_id)
        
        
        if patient.wallet.balance >= clinic.clinic_setting.cost :
            
            amount = int(clinic.clinic_setting.cost)

            payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # Adjust to your preferred currency
            payment_method_types=['card'],
            )
                        
            appointment =Appointment.objects.create(
                appointment_datetime=appointment_datetime,
                clinic=clinic,
                patient=patient,
            )
            
            
            payment_intent_obj = PaymentIntent.objects.create(
            user=request.user,
            appointment=appointment,
            intent_id=payment_intent.id,
            )
            
            slot.is_available = False
            slot.save()
            patient.wallet.balance = - clinic.clinic_setting.cost        
            patient.wallet.save()
            

            messages.success(request , 'نوبت شما با موفقیت ثبت شد')
            return redirect(clinicProfile , clinic_id)
        else : 
            messages.error(request , 'موجودی شما کافی نمیباشد')
            return redirect(clinicProfile , clinic_id)
    else:
        messages.error(request , 'زمان مورد نظر شما خالی نمیباشد')
        return redirect(clinicProfile , clinic_id)


from django.shortcuts import render
from datetime import datetime
from django.utils import timezone

@login_required
def todayAppointments(request ):
   

    today = timezone.now().date()
    clinic = Clinic.objects.get(user=request.user)
    appointments = Appointment.objects.filter(clinic=clinic,appointment_datetime__date=today)
    context = {'today_appointments': appointments}
    return render(request, 'clinics/clinicDashboard.html', context)
