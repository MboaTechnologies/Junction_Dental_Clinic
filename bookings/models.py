from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from Accounts.models import User
from Appointment.models import Appointment

from doctors.models import DoctorReg


class Booking(models.Model):
    doctor = models.ForeignKey(DoctorReg
        ,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    patient = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("no_show", "No Show"),
        ],
        default="pending",
    )

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        # Ensure no double bookings for same doctor at same time
        unique_together = ["doctor", "appointment_date", "appointment_time"]
    
    def __str__(self):
        if self.doctor.member:
            return f"Appointment with Dr.{self.doctor.member.first_name} {self.doctor.member.last_name} on {self.appointment_date} at {self.appointment_time} Call:  {self.doctor.member.mobile_number}"
        else:
            return f"User not associated - {self.mobile_number}"

   

class Prescription(models.Model):
    booking = models.OneToOneField(
        "Booking", on_delete=models.CASCADE, related_name="prescription"
    )
    doctor = models.ForeignKey(DoctorReg,
        on_delete=models.CASCADE,
        related_name="prescriptions_given",
    )
    patient = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="prescriptions_received",
    )
    symptoms = models.TextField()
    diagnosis = models.TextField()
    medications = RichTextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor}"

    class Meta:
        ordering = ["-created_at"]
