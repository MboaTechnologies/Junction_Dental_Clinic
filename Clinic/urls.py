from django.urls import path
from .views import *
from  Clinic.doc_views import *
urlpatterns = [
    path('', HeroView, name='hero'),
    path('Doctor/DocHome', doctor_home, name='doctor_home'),
    path('Doctor/ViewAppointment', View_Appointment, name='view_appointment'),
    path('DoctorPatientAppointmentDetails/<str:id>', Patient_Appointment_Details,name='patientappointmentdetails'),
    path('AppointmentDetailsRemark/Update', Patient_Appointment_Details_Remark,name='patient_appointment_details_remark'),
    path('DoctorPatientApprovedAppointment', Patient_Approved_Appointment, name='patientapprovedappointment'),
    path('DoctorPatientCancelledAppointment', Patient_Cancelled_Appointment,name='patientcancelledappointment'),
    path('DoctorPatientNewAppointment', Patient_New_Appointment, name='patientnewappointment'),
    path('DoctorPatientListApprovedAppointment', Patient_List_Approved_Appointment,name='patientlistappointment'),
    path('DoctorAppointmentList/<str:id>', DoctorAppointmentList, name='doctorappointmentlist'),
    path('PatientAppointmentPrescription', Patient_Appointment_Prescription,name='patientappointmentprescription'),
    path('PatientAppointmentCompleted', Patient_Appointment_Completed, name='patientappointmentcompleted'),
    path('SearchAppointment', Search_Appointments, name='search_appointment'),
    path('BetweenDateReport', Between_Date_Report, name='between_date_report'),

]
