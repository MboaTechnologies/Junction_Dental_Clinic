from django.db import models
from Accounts.models import User
from Clinic.models import Specialization


# Create your models here.
class DoctorReg(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    clinic_code = models.CharField(max_length=8)
    clinic_name = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=11)
    other_specializations_id = models.ManyToManyField(Specialization,)
    reg_date_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.member:
            return f"{self.member.first_name} {self.member.last_name} - {self.mobile_number}"
        else:
            return f"User not associated - {self.mobile_number}"
