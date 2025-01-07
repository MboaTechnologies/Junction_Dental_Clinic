from django.contrib import admin

# Register your models here.
from .models import Specialization, Page, DoctorReg

# Register your models here.

admin.site.register(DoctorReg)
admin.site.register(Specialization)
admin.site.register(Page)
