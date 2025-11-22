from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt, os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret123")

@api_view(['POST'])
def login_view(request):
    data = request.data
    username = data.get("email")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=1)},
        JWT_SECRET,
        algorithm="HS256"
    )

    return Response({"token": token})
