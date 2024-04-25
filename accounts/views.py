from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .utils import generate_otp, send_otp_phone
from .models import User
from .serializers import UserSerializer


class LoginWithOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        try:
            user, created = User.objects.get_or_create(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_phone(phone_number, otp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        otp = request.data.get('otp', '')

        user, created = User.objects.get_or_create(phone_number=phone_number)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        data = {"message": "Logout successful"}
        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
