from django.db.models.signals import post_save
from django.dispatch import receiver
from clinics.models import Clinic, ClinicSetting

@receiver(post_save, sender=Clinic)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        ClinicSetting.objects.create(clinic=instance)
        print("created")
    else:
        try:
            print("updated")
            profile = ClinicSetting.objects.get(clinic=instance)
            profile.save()
        except ClinicSetting.DoesNotExist:
            ClinicSetting.objects.create(clinic=instance)
            print("could not found but created")
