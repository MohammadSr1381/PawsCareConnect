from django.contrib import admin
from clinics.models import Clinic



class ClinicAdmin(admin.ModelAdmin):
    list_display = ('user' , 'clinic_name' , 'is_approver' , 'created_at')
    list_display_links = ('user' , 'clinic_name')

admin.site.register(Clinic , ClinicAdmin)