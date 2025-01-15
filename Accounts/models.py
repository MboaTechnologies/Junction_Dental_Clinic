from django.db import models
from .managers import UserManager
# from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from .constants import PATIENT_TYPE_CHOICES, SPECIALIZATION_CHOICES, GENDER_CHOICES
import string
import random


def generate_service_id():
    alphanumeric = string.ascii_uppercase + string.digits
    return ''.join(random.choices(alphanumeric, k=6))

# Create a Custom User Model


class User(AbstractUser):
    username = models.CharField(unique=True, null=False, max_length=50, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_Member_Patient = models.BooleanField(default=False)
    has_next_of_kin = models.BooleanField(default=False)
    next_of_kin = models.ForeignKey('NextOfKin', on_delete=models.CASCADE, blank=True, null=True)
    is_Doctor = models.BooleanField(default=False)
    specialization = models.CharField(max_length=19, blank=True, choices=SPECIALIZATION_CHOICES,)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=False, default='icon/bondijunction_dentalclinic_logo-300x258.jpg', blank=False)
    patient_type = models.CharField(max_length=50, null=True, choices=PATIENT_TYPE_CHOICES)
    patient_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    member_code = models.CharField(default=generate_service_id, max_length=6, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    # mobile_number = PhoneNumberField(max_length=13, blank=True, null=True, unique=True)
    mobile_number = models.CharField(max_length=13, blank=True, null=True, unique=True)
    registered = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def set_last_logout(self):
        self.last_logout = timezone.now()
        self.save(update_fields=['last_logout'])

    def next_of_kin_name(self):
        if self.has_next_of_kin:
            try:
                next_of_kin = NextOfKin.objects.get(related_patient=self)
                return f"{next_of_kin.kin_fname} {next_of_kin.kin_lname}"
            except NextOfKin.DoesNotExist:
                return "None"
        else:
            return "None"

    # Meta class to set metadata options
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


# Create a model for Next of Kin(for a Patient)
class NextOfKin(models.Model):
    RELATIONSHIP_CHOICES = [
        ('', '----------'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Aunt', 'Aunt'),
        ('Uncle', 'Uncle'),
        ('Niece', 'Niece'),
        ('Nephew', 'Nephew'),
        ('Cousin', 'Cousin'),
        ('Other close Relative', 'Other close Relative'),
        ('Wife', 'Wife'),
        ('Husband', 'Husband'),
        ('Guardian', 'Guardian'),
    ]

    kin_first_name = models.CharField(max_length=50)
    kin_code = models.CharField(max_length=15, unique=True, blank=True, null=True)
    kin_last_name = models.CharField(max_length=50)
    related_patient = models.ForeignKey(
        User,
        verbose_name='Related Patient',
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_Member_Patient=True) | Q(mobile_number=True)
    )
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    # kin_mobile_number = PhoneNumberField(max_length=13, blank=True, null=True, unique=False)
    kin_mobile_number = models.CharField(max_length=13, blank=True, null=True, unique=False)
    registered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.kin_fname} {self.kin_lname}"

    class Meta:
        verbose_name = "Next of Kin"
        verbose_name_plural = "Next of Kins"





# Create a method to generate a random appointment ID
# Create a model for OTP(One Time Password)


class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    otp_created = models.DateTimeField(default=timezone.now)
    otp_verified = models.BooleanField(default=False)
    for_email = models.EmailField(null=True, blank=True, default="")

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices('0123456789', k=6))

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
