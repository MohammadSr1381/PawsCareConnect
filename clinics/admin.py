from django.contrib import admin
from clinics.models import Clinic, ClinicSetting, Comment, Rating

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('user', 'clinic_name', 'is_approver', 'created_at')
    list_display_links = ('user', 'clinic_name')

admin.site.register(Clinic, ClinicAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'clinic', 'comment_text', 'created_at')
    list_display_links = ('patient', 'clinic')

admin.site.register(Comment, CommentAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'clinic', 'score', 'created_at')
    list_display_links = ('patient', 'clinic')

admin.site.register(Rating, RatingAdmin)

class ClinicSettingAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'cost', 'opening_time', 'closing_time')
    list_display_links = ('clinic', 'cost')

admin.site.register(ClinicSetting, ClinicSettingAdmin)
