from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager



class UserManager(BaseUserManager):
    
    def create_user(self , first_name , last_name , phone_number , email , password = None):
        
        if not email :
            raise ValueError("user must have an email address")
        
        if not phone_number :
            raise ValueError("user must have a phone number")
        
        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            first_name = first_name,
            last_name = last_name,  
        )        
        user.set_password(password)
        user.save(using = self._db)
        
        return user               
    
    
    
    def create_superuser(self , first_name , last_name , phone_number , email , password = None):
        
        user = self.create_user(
            email = self.normalize_email(email),
            phone_number= phone_number,
            password= password,
            first_name = first_name,
            last_name = last_name,)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        
        return user               
    

class User(AbstractBaseUser):

    PATIENT = 1
    CLINIC = 2
    LABORATORY = 3
    
    ROLE_CHOICE = (
        (PATIENT , 'Patient'),
        (CLINIC , 'Clinic'),
        (LABORATORY , "Laboratory"),
    )
    
    
    
    
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100 , unique=True)
    phone_number = models.CharField(max_length= 12 , unique=True)
    role = models.PositiveBigIntegerField(choices=ROLE_CHOICE , blank=True , null=True)
    
    data_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_data = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number' , 'first_name' , 'last_name']
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self , perm , obj = None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Patient'
        elif self.role == 2:
            user_role = 'Clinic'
        else :
            user_role = 'Laboratory'


class UserProfile(models.Model):
    
    
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE , blank= True , null=True)
    profile_picture = models.ImageField(upload_to='users/profile_picture' , blank=True , null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos' , blank=True , null=True)
    citizen_id = models.CharField(max_length=10 , blank=True , null=True) 
    city = models.PositiveBigIntegerField(choices=LOCATION_CHOICE , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.email


class Permission(models.Model):
    
    name = models.CharField(max_length=50 , default='permission')

    patientRating = models.BooleanField(default=False)
    patientComment = models.BooleanField(default=False)
    patientSignUp = models.BooleanField(default=False)
    patientLogin = models.BooleanField(default=False)
    clinicRating = models.BooleanField(default=False)
    clinicComment = models.BooleanField(default=False)
    clinicSignUp = models.BooleanField(default=False)
    clinicLogin = models.BooleanField(default=False)
    askQuestion = models.BooleanField(default=False)
    answerQuestion = models.BooleanField(default=False)
    patientAppointment = models.BooleanField(default=False)
    clinicAppointment = models.BooleanField(default=False)
    
    _singleton_instance = None

    def save(self, *args, **kwargs):
        if not self.pk and Permission.objects.exists():
            raise Permission.DoesNotExist(
                "There can only be one Permission instance. Edit the existing instance."
            )
        super().save(*args, **kwargs)
        Permission._singleton_instance = self

    @classmethod
    def get_singleton(cls):
        # Get or create the singleton instance
        if cls._singleton_instance is None:
            cls._singleton_instance, created = cls.objects.get_or_create(pk=1)
        return cls._singleton_instance
    
    