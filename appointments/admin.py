from django.contrib import admin

from appointments.models import Appointment, AppointmentSlot

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'clinic', 'appointment_datetime', 'status' , 'notes')
    list_display_links = ('patient', 'clinic', 'appointment_datetime')
    
admin.site.register(Appointment, AppointmentAdmin)


class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ( 'clinic', 'date', 'start_time' , 'end_time' , 'is_available')
    
admin.site.register(AppointmentSlot, AppointmentSlotAdmin)