from django.db.models.signals import post_save
from django.dispatch import receiver
from patients.models import Patient, Wallet




@receiver(post_save, sender=Patient)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(patient=instance)
        print("Wallet created")
    else:
      
        wallet, wallet_created = Wallet.objects.get_or_create(patient=instance)
        if wallet_created:
            print("Wallet not found, created new one")
        else:
            print("Wallet found and updated")

 
    