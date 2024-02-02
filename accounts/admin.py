from django.contrib import admin
from .models import  User , UserProfile
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    
    list_display = ('email' , 'first_name' , 'last_name' , 'phone_number','role' , 'is_active')
    ordering = ('-data_join',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User , CustomUserAdmin)
admin.site.register(UserProfile)

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Permission

class PermissionAdminForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'

    def clean(self):
        if Permission.objects.exists() and not self.instance.pk:
            raise ValidationError("There can only be one Permission instance. Edit the existing instance.")


class PermissionAdmin(admin.ModelAdmin):
    form = PermissionAdminForm
    list_display = ['name','patientRating', 'patientComment', 'patientSignUp', 'patientLogin',
                    'clinicRating', 'clinicComment', 'clinicSignUp', 'clinicLogin' , 'askQuestion' , 'answerQuestion' , 'patientAppointment','clinicAppointment']

admin.site.register(Permission, PermissionAdmin)


