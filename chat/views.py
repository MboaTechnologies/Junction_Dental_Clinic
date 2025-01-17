from .utils import send_sms


def send_verification_code(request):
    # Get user's phone number from the request
    phone_number = request.POST.get('phone_number')
    # Generate a random verification code
    verification_code = generate_verification_code()
    # Save the verification code in the database or session for later verification
    # Send the verification code via SMS
    message = f"Your verification code is: {verification_code}"
    send_sms(phone_number, message)
    return render(request, 'verification_code_sent.html')