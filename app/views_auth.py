# app/views_auth.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def signup_view(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Email and password required'}, status=400)

    if User.objects.filter(username=email).exists():
        return JsonResponse({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    user.save()

    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'email': email
    })


@api_view(['POST'])
def login_view(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    user = authenticate(username=email, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'email': email
    })


@api_view(['POST'])
def password_reset_view(request):
    # Simple placeholder: Implement email sending logic here
    email = request.data.get('email')
    if not email:
        return JsonResponse({'error': 'Email required'}, status=400)
    # You can integrate Django's password reset later
    return JsonResponse({'message': f'Password reset link sent to {email}'})
