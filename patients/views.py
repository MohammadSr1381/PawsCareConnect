from decimal import Decimal, InvalidOperation
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from site import USER_BASE
from django.shortcuts import redirect, render
from accounts.forms import UserForm, userProfileForm
from accounts.models import User, UserProfile
from django.contrib import messages
from clinics.models import Clinic
from patients.models import Patient, Question, Wallet 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def pprofile(request):
    
    user_instance = User.objects.get(id=request.user.id)
    prof_instance = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
        print(citizen_id)
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
        
        return render(request, 'patients/patientDashboard.html', context)

def showWalletInfo(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    wallet = wallet = Wallet.objects.get(patient=patient)
    print(f"Wallet Balance: {wallet.balance}")

    context = {
        'wallet' : wallet
    }
    
    return render(request, 'patients/patientDashboard.html', context)

@require_POST
def increaseBalance(request):
    
    amount_str = request.POST.get('amount', '0')
    try:
        amount = Decimal(amount_str)
    except InvalidOperation:  # Catch InvalidOperation from the decimal module
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
        wallet.balance += Decimal(amount)
        wallet.save()

        messages.success(request, f'موجودی با مبلغ {amount} تومان افزایش یافت.')
        
    else:
        messages.error(request, 'مبلغ میتواند بین 10 هزار تا 200 هزار تومان باشد')
        return redirect('pprofile')
    
    
    return render(request , 'patients/patientDashboard.html')