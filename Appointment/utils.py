from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail


def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )



CARRIER_EMAIL_GATEWAYS = {
    "safaricom": "{number}@safaricom.sms.gateway",  # Replace with Safaricom's actual SMS gateway
    "airtel": "{number}@airtel.sms.gateway",        # Replace with Airtel's SMS gateway
    "telkom": "{number}@telkom.sms.gateway",        # Replace with Telkom's SMS gateway
}

def get_carrier_from_number(phone_number):
    # Identify carrier by prefix
    safaricom_prefixes = ('070', '071', '072', '074', '079')
    airtel_prefixes = ('073', '075')
    telkom_prefixes = ('076', '077')

    prefix = phone_number[:3]
    if prefix in safaricom_prefixes:
        return "safaricom"
    elif prefix in airtel_prefixes:
        return "airtel"
    elif prefix in telkom_prefixes:
        return "telkom"
    return None  # Unknown carrier

def send_sms_via_email(phone_number, message):
    carrier = get_carrier_from_number(phone_number)
    if not carrier:
        raise ValueError(f"Could not determine carrier for phone number: {phone_number}")

    email_gateway = CARRIER_EMAIL_GATEWAYS.get(carrier)
    if not email_gateway:
        raise ValueError(f"Carrier {carrier} does not have an email-to-SMS gateway configured.")

    # Format the recipient email address
    recipient_email = email_gateway.format(number=phone_number)

    # Send the SMS via email
    send_mail(
        subject='',  # Subject not required for SMS
        message=message,
        from_email='mboaacademy@gmail.com',
        recipient_list=[recipient_email],
    )