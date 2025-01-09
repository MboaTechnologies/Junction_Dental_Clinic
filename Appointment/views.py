from .models import Appointment
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Clinic.models import DoctorReg, Page, Specialization
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from Accounts.models import User


def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    worry = Specialization.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointment_number = random.randint(100000000, 999999999)
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        worry_id = request.POST.get('worry_need')
        additional_msg = request.POST.get('additional_msg')

        # Retrieve the DoctorReg instance using the doctor_id
        doc_instance = DoctorReg.objects.get(id=doctor_id)
        worry_instance = Specialization.objects.get(id=worry_id)

        # Validate that date_of_appointment is greater than today's date
        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                # If the appointment date is not in the future, display an error message
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('appointment')  # Redirect back to the appointment page
        except ValueError:
            # Handle invalid date format error
            messages.error(request, "Invalid date format")
            return redirect('appointment')  # Redirect back to the appointment page

        # Create a new Appointment instance with the provided data
        appointment_details = Appointment.objects.create(
            appointment_number=appointment_number,
            fullname=full_name,
            email=email,
            mobile_number=mobile_number,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            worry_id=worry_instance,
            additional_msg=additional_msg
        )

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exist')
            return redirect('/accounts/login/')
        if User.objects.filter(username=full_name).exists():
            messages.warning(request, 'Account exist on Membership Plan')
            return redirect('/accounts/login/')

        # Display a success message
        messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
        appointment_details.save()
        return redirect('/accounts/login/')

    context = {'doctorview': doctorview, 'worry': worry,
               'page': page}
    return render(request, 'appointment/appointment.html', context)


def User_Search_Appointments(request):
    page = Page.objects.all()

    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(
                appointment_number__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'appointment/search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'appointment/userbase.html ', context)

    # If the request method is not GET
    context = {'page': page}
    return render(request, 'appointment/userbase.html', context)


def user_profile_history_appointment(request):
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


def View_Appointment_Details(request, id):
    page = Page.objects.all()
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails,
               'page': page

               }

    return render(request, 'appointment/user_appointment-details.html', context)


@login_required(login_url='/')
def View_Appointment(request):
    try:
        doctor_reg = DoctorReg.objects.get(admin=request.user)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)

        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 10 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {'error_message': str(e)}

    return render(request, 'appointment/view_appointment.html', context)


@login_required(login_url='/')
def DOCTORHOME(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    allaptcount = Appointment.objects.filter(doctor_id=doctor_reg).count
    newaptcount = Appointment.objects.filter(status='0', doctor_id=doctor_reg).count
    appaptcount = Appointment.objects.filter(status='Approved', doctor_id=doctor_reg).count
    canaptcount = Appointment.objects.filter(status='Cancelled', doctor_id=doctor_reg).count
    comaptcount = Appointment.objects.filter(status='Completed', doctor_id=doctor_reg).count
    context = {
        'newaptcount': newaptcount,
        'allaptcount': allaptcount,
        'appaptcount': appaptcount,
        'canaptcount': canaptcount,
        'comaptcount': comaptcount

    }
    return render(request, 'doc/dochome.html', context)


def Patient_Appointment_Details(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }

    return render(request, 'doc_profile/patient_appointment_details.html', context)


def Patient_Appointment_Details_Remark(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        remark = request.POST['remark']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.remark = remark
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, "Status Update successfully")
        context = {'patientaptdet': patientaptdet}
        return render(request, 'doc_profile/view_appointment.html', context)

    return redirect('view_appointment')


def Patient_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved', doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)


def Patient_Cancelled_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Cancelled', doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc_profile/patient_app_appointment.html', context)


def Patient_New_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='0', doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc_profile/patient_app_appointment.html', context)


def Patient_List_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved', doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc_profile/patient_list_app_appointment.html', context)


def DoctorAppointmentList(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }
    return render(request, 'doc_profile/doctor_appointment_list_details.html', context)


def AppointmentHistoryList(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }
    return render(request, 'doc_profile/doctor_appointment_list_details.html', context)


def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        prescription = request.POST['prescription']
        recommendedtest = request.POST['recommendedtest']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, "Status Update successfully")
        context = {'patientaptdet': patientaptdet}
        return render(request, 'doc_profile/patient_list_app_appointment.html', context)
    return redirect('view_appointment')


def Patient_Appointment_Completed(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Completed', doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc_profile/patient_list_app_appointment.html', context)


def Search_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(
                appointmentnumber__icontains=query) & Appointment.objects.filter(doctor_id=doctor_reg)
            messages.success(request, "Search against " + query)
            return render(request, 'doc_profile/search-appointment.html', {'patient': patient, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'doc_profile/search-appointment.html', {})


def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doc_profile/between-dates-report.html',
                          {'visitor': patient, 'error_message': 'Invalid date format'})

        # Filter Appointment between the given date range
        patient = Appointment.objects.filter(created_at__range=(start_date, end_date)) & Appointment.objects.filter(
            doctor_id=doctor_reg)

    return render(request, 'doc_profile/between-dates-report.html',
                  {'patient': patient, 'start_date': start_date, 'end_date': end_date})
