from multiprocessing import context
from django.shortcuts import render
from site import USER_BASE
from django.shortcuts import redirect, render
from accounts.forms import UserForm, userProfileForm
from accounts.models import User, UserProfile
from django.contrib import messages
from clinics.models import Clinic
from patients.models import Patient, Question 
from django.contrib.auth.decorators import login_required


def pprofile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    prof_instance = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
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
            prof_instance.citizen_id = citizen_id
            prof_instance.save()

            messages.success(request, "پروفایل شما با موفقیت آپدیت شد")
            return redirect('pprofile')

    else:
        profile_form = userProfileForm(instance=user_instance.userprofile)
        context = {
            'user': user_instance,
            'profile_form': profile_form,
        }
        return render(request, 'patients/patientDashboard.html', context)
    

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
        messages.success(request,'question asked')
        return redirect('home')
        
    return render(request, 'temporary/askQuestion.html', context)

