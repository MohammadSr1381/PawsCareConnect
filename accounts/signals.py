from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User , UserProfile



@receiver(post_save , sender = User)
def post_save_create_profile_receiver(sender , instance , created , **kwargs):
    if created :
        UserProfile.objects.create(user = instance)
        print("created")
    else :
        try:
            print("updated")
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            
        except:
            UserProfile.objects.create(user = instance)
            print("couldnt found but created ")

            
 
    