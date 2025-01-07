from django.db import models
from Accounts.models import User
import string
import random


def generate_service_id():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric, k=6))


class Specialization(models.Model):
    service_code = models.CharField(default=generate_service_id, null=True,  max_length=6, )
    sname = models.CharField(max_length=100, null=True,)
    service_title = models.CharField(max_length=225, null=True,)
    service_image = models.ImageField(upload_to='services_image/', null=True, blank=True)
    service_logo = models.ImageField(upload_to='service_logo/', null=True, blank=True)
    service_price = models.IntegerField(null=True, blank=False)
    ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname


class DoctorReg(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"


class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle