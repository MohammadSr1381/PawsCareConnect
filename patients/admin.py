from django.contrib import admin
from .models import Patient, Wallet, Question


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user' , 'user_profile' , 'created_at' , 'modified_at')
    
    

class WalletAdmin(admin.ModelAdmin):
    list_display = ('patient' , 'balance' , 'is_activated' , 'created_at' ,'modified_at')
    
 
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('patient' , 'clinic' , 'question_text' , 'answer_text')
    
    
admin.site.register(Patient , PatientAdmin)
admin.site.register(Wallet , WalletAdmin)
admin.site.register(Question , QuestionAdmin)
