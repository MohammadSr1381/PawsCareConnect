from django.db import models
from accounts.models import User, UserProfile



class Clinic(models.Model):
    
    TEHRAN = 1
    TABRIZ = 2
    ESFAHAN = 3
    SHIRAZ = 4
    KARAJ = 5
    MASHHAD = 6
    GOM = 7
    AHVAZ = 8
    KERMANSHAH = 9
    RASHT = 10
    URMIA = 11
    ZAHEDAN = 12
    HAMADAN = 13
    KERMAN = 14
    YAZD = 15
    ARDABIL = 16
    BANDARABAS = 17
    ARAK = 18
    
    LOCATION_CHOICE = (
    (TEHRAN, 'Tehran'),
    (TABRIZ, 'Tabriz'),
    (ESFAHAN, 'Esfahan'),
    (SHIRAZ, 'Shiraz'),
    (KARAJ, 'Karaj'),
    (MASHHAD, 'Mashhad'),
    (GOM, 'Gom'),
    (AHVAZ, 'Ahvaz'),
    (KERMANSHAH, 'Kermanshah'),
    (RASHT, 'Rasht'),
    (URMIA, 'Urmia'),
    (ZAHEDAN, 'Zahedan'),
    (HAMADAN, 'Hamadan'),
    (KERMAN, 'Kerman'),
    (YAZD, 'Yazd'),
    (ARDABIL, 'Ardabil'),
    (BANDARABAS, 'BandarAbbas'),
    (ARAK, 'Arak'),
    )
    
    
    user = models.OneToOneField(User , related_name='user' , on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile , related_name='userprofile' , on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=100)
    citizen_id = models.CharField(max_length=10)
    city = models.PositiveBigIntegerField(choices=LOCATION_CHOICE , blank=True , null=True)
    address = models.CharField(max_length=150)
    clinic_license = models.ImageField(upload_to='clinic/license')
    is_approver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.clinic_name