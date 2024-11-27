# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from mysql_models.models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from .serializers import CustomUserSerializer
from dotenv import load_dotenv
import os
load_dotenv()
# User = get_user_model()


class BuiltInRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        # Validation checks
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        # User creation
        try:
            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)
            new_user = CustomUser.objects.create(
                email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            new_user.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuiltInLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            if not CustomUser.objects.filter(email=email).exists():
                return Response({"data": {}, "error": "Account with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if not CustomUser.objects.filter(email=email, password=password).exists():
                return Response({"data": {}, "error": "Invald credentials"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.get(email=email, password=password)
            user_serializer = CustomUserSerializer(user)
            return Response({"data": user_serializer.data, "message": "User logged in successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": {}, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_OAUTH2_CLIENT_ID'))
            print(id_info)
            email = id_info.get("email")
            first_name = id_info.get("given_name")
            last_name = id_info.get("family_name")

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={"first_name": first_name, "last_name": last_name, "username": email}
            )

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)