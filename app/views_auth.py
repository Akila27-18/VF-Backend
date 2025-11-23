from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status

@api_view(['POST'])
def password_reset(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=404)

    # Generate a temporary password or token (simple approach)
    temp_password = get_random_string(8)
    user.set_password(temp_password)
    user.save()

    # Send email (update your SMTP settings in settings.py)
    send_mail(
        subject="Password Reset Request",
        message=f"Hello {user.first_name},\n\nYour temporary password is: {temp_password}\nPlease login and change your password immediately.",
        from_email="no-reply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({"message": "Temporary password sent to your email"})
