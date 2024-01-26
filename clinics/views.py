from site import USER_BASE
from django.shortcuts import redirect, render
from accounts.forms import UserForm, userProfileForm
from accounts.models import User, UserProfile
from clinics.forms import CRUDClinicForm, CRUDUserForm, CRUDUserProfileForm, ClinicForm
from clinics.models import Clinic
from django.contrib import messages 


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
        profile_form = userProfileForm(instance=user_instance.userprofile)
        clinic_form = ClinicForm(instance=clinic_instance)
        context = {
            'user': user_instance,
            'profile_form': profile_form,
            'clinic_form': clinic_form,
            'location_choices': clinic_instance.LOCATION_CHOICE 
        }
        return render(request, 'clinics/clinicDashboard.html', context)



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