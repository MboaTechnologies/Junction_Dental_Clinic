from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout
from .models import User
from Clinic.models import Page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Clinic.models import Specialization
from Appointment.models import Appointment


# Create your views here.

def index(request):
    return render(request, 'accounts/sign-up.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/accounts/login/')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = LoginForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm


def user_logout_view(request):
    logout(request)
    return redirect('/accounts/login/')



def user_profile_view(request):
    user_view = request.user
    page = Page.objects.all()
    Services = Specialization.objects.all()
    context = {'services': Services, 'page': page}
    Appointment_History = Appointment.objects.filter(email__icontains=user_view) | Appointment.objects.filter(
        mobile_number__icontains=user_view)
    if Appointment_History:
        # Filter records where fullname or Appointment Number contains the query
        Appointee = Appointment_History
        messages.info(request, 'Your Appointment History Exists')
        context = {'Appointee': Appointee, 'user_view': user_view, 'page': page, 'services': Services, }
        return render(request, 'user_profile/profile.html', context)
    return render(request, 'user_profile/user_profile.html', context)


def user_profile(request):
    user_view = request.user
    page = Page.objects.all()
    Services = Specialization.objects.all()
    context = {'services': Services, 'page': page}
    Appointment_History = Appointment.objects.filter(email__icontains=user_view) | Appointment.objects.filter(
        mobile_number__icontains=user_view)
    if Appointment_History:
        # Filter records where fullname or Appointment Number contains the query
        Appointee = Appointment_History
        messages.info(request, 'Your Appointment History Exists')
        context = {'Appointee': Appointee, 'user_view': user_view, 'page': page, 'services': Services, }
        return render(request, 'user_profile/profile.html', context)
    return render(request, 'user_profile/profile.html', context)


@login_required(login_url='/')
def profile_Update(request):
    member = User.objects.get(email=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            profile_photo = member.profile_photo
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            username = request.POST.get('username')
            try:
                if request.FILES.get('image') is not None:
                    profile_photo = request.FILES.get('profile_picture')

                member.profile_photo = profile_photo
                member.phone_number = phone_number
                member.first_name = first_name
                member.username = username
                member.email = email
                member.last_name = last_name
                member.save()

            except:
                messages.error(request, "Your profile updation has been failed")
        return render(request, 'user_profile/user_profile_update.html')
    return render(request, 'user_profile/user_profile_update.html')

