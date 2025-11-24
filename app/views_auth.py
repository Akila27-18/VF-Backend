from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """
    Sign up a new user using email and password.
    Returns JWT access and refresh tokens.
    """
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
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'email': email
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user and return JWT tokens.
    """
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Email and password required'}, status=400)

    user = authenticate(username=email, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'email': email
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_view(request):
    """
    Placeholder for password reset.
    In production, integrate Django’s password reset flow.
    """
    email = request.data.get('email')
    if not email:
        return JsonResponse({'error': 'Email required'}, status=400)

    # TODO: Integrate Django’s password reset email logic
    return JsonResponse({'message': f'Password reset link sent to {email}'})
