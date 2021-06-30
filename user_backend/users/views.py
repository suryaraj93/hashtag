from contextvars import Token

from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import LoginSerializer, UserSerializer

# Create your views here.


class Userview(APIView):

    def get(self, request, format=None):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": "Registeration Successful",
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Registration failed",
                "data": serializer.data,
            },
            status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        djangologin(request, user)
        token, created = Token.objects.get_or_create(user=user)
        request.session['token'] = token.key
        return Response(
            {
                'message': 'You have successfully Logged in.',
                'user': user.name,
                'token': token.key
            },
            status=status.HTTP_200_OK)


class Logout(APIView):

    def post(self, request):
        djangologout(request)
        return Response(
            {
                'message': 'You have Logged out successfully.'
            },
            status=status.status.HTTP_204_NO_CONTENT)
