from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Appointment
from django.db import transaction


class PatientAppointmentForm(forms.ModelForm):
    fullname = forms.CharField(
        label=_("Full name"),
        widget=forms.CharField(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
    )

    class Meta:
        model = Appointment
        fields = ('fullname', '', 'additional_msg', 'worry_id', 'doctor_id', 'time_of_appointment', 'date_of_appointment', 'mobile_number', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }


class DoctorAppointRegistrationForm(forms.ModelForm):
    appointment_number = forms.ModelChoiceField(
        queryset=Appointment.objects.all()
    )
    doctor_id = forms.ModelChoiceField(queryset=Appointment.objects.all
    ()
                                       )
    time_of_appointment = forms.TimeField()
    date_of_appointment = forms.DateField()

    class Meta:
        model = Appointment
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')

            Appointment.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                account_type=account_type,
                account_no=(
                    user.id +
                    int(12834)
                )
            )
        return user
