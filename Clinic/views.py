from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import Specialization, Page
from Dashboard.models import DoctorReg
from Appointment.models import Appointment
from datetime import datetime
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.http import JsonResponse
from .utils import send_sms
from django.shortcuts import render
from urllib.parse import urlencode
 

def generate_whatsapp_link(request):
    phone_number = "254708534184"
    base_url = f"https://wa.me/{phone_number}"
    message = "Hello! I'd like to book an appointment for dental services."
    encoded_message = urlencode({'text': message})
    whatsapp_url = f"{base_url}?{encoded_message}"

    return render(request, 'template_name.html', {'whatsapp_url': whatsapp_url})


@login_required(login_url='/')
def doctor_home(request):
    doctor_count = DoctorReg.objects.all().count
    context = {
        'doctor_count': doctor_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='/')
def Specialization(request):
    if request.method == "POST":
        specializationname = request.POST.get('specializationname')
        specialization = Specialization(
            sname=specializationname,
        )
        specialization.save()
        messages.success(request, 'Specialization  Added Succeesfully!!!')
        return redirect("add_specilizations")
    return render(request, 'admin/specialization.html')


@login_required(login_url='/')
def Manage_Specialization(request):
    specialization = Specialization.objects.all()
    context = {'specialization': specialization,

               }
    return render(request, 'admin/manage_specialization.html', context)


def Delete_Specialization(request, id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')

    return redirect('manage_specilizations')


login_required(login_url='/')


def Update_Specialization(request, id):
    specialization = Specialization.objects.get(id=id)

    context = {
        'specialization': specialization,
    }

    return render(request, 'admin/update_specialization.html', context)


login_required(login_url='/')


def Update_Specialization_Details(request):
    if request.method == 'POST':
        sep_id = request.POST.get('sep_id')
        sname = request.POST.get('sname')
        sepcialization = Specialization.objects.get(id=sep_id)
        sepcialization.sname = sname
        sepcialization.save()
        messages.success(request, "Your specialization detail has been updated successfully")
        return redirect('manage_specilizations')
    return render(request, 'admin/update_specialization.html')


@login_required(login_url='/')
def DoctorList(request):
    doctorlist = DoctorReg.objects.all()
    context = {'doctorlist': doctorlist,

               }
    return render(request, 'admin/doctor-list.html', context)


def ViewDoctorDetails(request, id):
    doctorlist1 = DoctorReg.objects.filter(id=id)
    context = {'doctorlist1': doctorlist1

               }

    return render(request, 'admin/doctor-details.html', context)


def ViewDoctorAppointmentList(request, id):
    patientdetails = Appointment.objects.filter(doctor_id=id)
    context = {'patientdetails': patientdetails

               }

    return render(request, 'admin/doctor_appointment_list.html', context)


def ViewPatientDetails(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }

    return render(request, 'admin/patient_appointment_details.html', context)


def Search_Doctor(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchdoc = DoctorReg.objects.filter(mobilenumber__icontains=query) | DoctorReg.objects.filter(
                admin__first_name__icontains=query) | DoctorReg.objects.filter(admin__last_name__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-doctor.html', {'searchdoc': searchdoc, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'admin/search-doctor.html', {})


def Doctor_Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    doctor = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/doctor-between-date.html',
                          {'doctor': doctor, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        doctor = DoctorReg.objects.filter(regdate_at__range=(start_date, end_date))

    return render(request, 'admin/doctor-between-date.html',
                  {'doctor': doctor, 'start_date': start_date, 'end_date': end_date})


@login_required(login_url='/')
def Website_Update(request):
    page = Page.objects.all()
    context = {"page": page,

               }
    return render(request, 'admin/website.html', context)


@login_required(login_url='/')
def Update_Website_Details(request):
    if request.method == 'POST':
        web_id = request.POST.get('web_id')
        pagetitle = request.POST['pagetitle']
        address = request.POST['address']
        aboutus = request.POST['aboutus']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        page = Page.objects.get(id=web_id)
        page.pagetitle = pagetitle
        page.address = address
        page.aboutus = aboutus
        page.email = email
        page.mobilenumber = mobilenumber
        page.save()
        messages.success(request, "Your website detail has been updated successfully")
        return redirect('website_update')
    return render(request, 'admin/website.html')


def HeroView(request):
    return render(request, "clinic/index.html")


def sms_reply(request):
    response = MessagingResponse()
    response.message("Thank you for your message!")
    return HttpResponse(str(response), content_type="text/xml")




def send_sms_view(request):
    to = request.GET.get('to')  # e.g., "+1234567890"
    message = request.GET.get('message', 'Hello from Twilio!')

    if not to:
        return JsonResponse({"error": "Recipient number is required."}, status=400)

    sms = send_sms(to, message)

    if sms:
        return JsonResponse({"success": f"Message sent to {to}"})
    return JsonResponse({"error": "Failed to send message."}, status=500)


