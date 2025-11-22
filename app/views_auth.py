from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret123")

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token = jwt.encode({'user_id': user.id}, JWT_SECRET, algorithm='HS256')
    return Response({'token': token})
