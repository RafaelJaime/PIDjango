from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializer import UserSerializer
# Create your views here.
class User_API(APIView):
    def get(self, request, format=None, *args, **kwargs):
        return Response({'successful': True, 'data':{'firstname':request.user.first_name, 'lastname':request.user.last_name}})
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "user" not in data or "password" not in data:
            return Response('Wrong credentials', status = status.HTTP_401_UNAUTHORIZED)

        user = user = authenticate(username=data["user"], password=data["password"])
        if not user:
            return Response({'successful': False, 'error':'Bad credentials'}, status=status.HTTP_404_NOT_FOUND)
        else:
            token = Token.objects.get_or_create(user=user)
            return Response({'successful': True, 'data':{'token':token[0].key}})
    @permission_classes([IsAuthenticated])
    def delete(self, request, format=None, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'successful': True, 'data':{'message':'Token removed successful.'}})
class TestView(APIView):
    def get(self, request, format=None):
        return Response({'detail': "GET Response"})
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "user" not in data or "password" not in data:
            return Response('Wrong credentials', status = status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(username=data["user"], password=data["password"])
        if not user:
            return Response('No default user, pleas create one', status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            token = Token.objects.get_or_create(user=user)
            return Response({'successful': True, 'detail':'POST answer', 'token':token[0].key})
        else:
            return Response('Not enought permisson, just superuser can get this information', status = status.HTTP_401_UNAUTHORIZED)