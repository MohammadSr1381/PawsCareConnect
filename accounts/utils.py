


from django.shortcuts import redirect


def detectUser(user):
    if user.role == 1 :
        redirectUrl = 'patientDashboard'
        return redirectUrl
    
    elif user.role == 2 :
        redirectUrl = 'clinicDashboard'
        return redirectUrl

    elif user.role == 3 :
        redirectUrl = 'laboratoryDashboard'
        return redirectUrl
    else :
        redirectUrl ='/admin'
        return redirectUrl
