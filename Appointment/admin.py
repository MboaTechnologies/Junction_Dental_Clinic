from django.contrib import admin
from .models import Appointment
from Accounts.models import User

# Register your models here.


admin.site.register(Appointment)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_number',
                    'email',
                    'fullname',
                    'mobile_number',
                    'date_of appointment',
                    'time_of_appointment',
                    'doctor_id',
                    'additional_msg',
                    'status',
                    'created_at',
                    'recommended_test',)
    ordering = ('created_at',)
    list_filter = ('appoint_id', 'appoint_area', ('appointed_doctor', admin.RelatedOnlyFieldListFilter),
                   ('appointee', admin.RelatedOnlyFieldListFilter), 'appoint_status', 'appoint_time', 'book_time',
                   'approve_date', 'close_date')

    search_fields = ('appoint_id',
                     'book_time',
                     'appoint_time',
                     'appoint_area',
                     'appoint_status',
                     'appointee__first_name',
                     'appointee__last_name',
                     'appointee__patient_id',
                     'appointee__patient_type',
                     'appointee__gender',
                     'appointee__email',
                     'appointee__mobile_number',
                     'appointee__username',
                     'appointed_doctor__gender',
                     'appointed_doctor__first_name',
                     'appointed_doctor__last_name',
                     'appointed_doctor__username',
                     'appointed_doctor__mobile_number',
                     'appointed_doctor__email',
                     'appointed_doctor__specialization',
                     )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointed_doctor':
            kwargs["queryset"] = User.objects.filter(is_Doctor=True)
        elif db_field.name == 'appointee':
            kwargs["queryset"] = User.objects.filter(is_Member_Patient=True) | User.objects.filter(
                is_New_Patient=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
