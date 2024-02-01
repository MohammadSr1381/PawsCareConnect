from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages , auth
from clinics.views import clinicProfile
from .models import Appointment, AppointmentSlot, Clinic , Patient
from django.contrib.auth.decorators import login_required


@login_required
def create_appointment(request, clinic_id, slot_id):
    
    if request.user.role != 1 :
        messages.error(request , 'کلینیک ها نمیتوانند راجع به یکدیگر نظر بدهند')
        return redirect(clinicProfile , clinic_id=clinic_id)
    slot = AppointmentSlot.objects.get(id=slot_id)


    opening_hour = slot.start_time
    today_date = datetime.now().date()
    appointment_datetime = datetime.combine(today_date, opening_hour)
    
    if slot.is_available:
        clinic = Clinic.objects.get(id=clinic_id)
        patient = Patient.objects.get(user=request.user)
        Appointment.objects.create(
            appointment_datetime=appointment_datetime,
            clinic=clinic,
            patient=patient,
        )
        slot.is_available = False
        slot.save()
        patient.wallet.balance =- clinic.clinic_setting.cost        
        patient.wallet.save()
        

        messages.success(request , 'نوبت شما با موفقیت ثبت شد')
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
