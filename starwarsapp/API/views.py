from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework import viewsets

from .serializer import UserSerializer, ArticleSerializer, EventSerializer, ArticlesSerializer

from account.models import User
from .models import Article, Event
# Create your views here.


class User_API(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, format=None, *args, **kwargs):
        return Response({'successful': True, 'data': {'firstname': request.user.first_name, 'lastname': request.user.last_name}})

    def post(self, request, format=None, *args, **kwargs):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "username" not in data or "password" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)

        user = user = authenticate(
            username=data["username"], password=data["password"])
        if not user:
            return Response({'successful': False, 'error': 'Bad credentials'}, status=status.HTTP_404_NOT_FOUND)
        else:
            token = Token.objects.get_or_create(user=user)
            return Response({'successful': True, 'data': {'token': token[0].key}})

    def put(self, request, format=None):
        user = User.objects.create_user(
            request.data['username'], password=request.data['password'])
        if user:
            return Response({'successful': True, 'data': {'username': request.data['username'], 'password': request.data['password']}})
        return Response({'successful': False, 'message': 'Bad credentials'})

    @permission_classes([IsAuthenticated])
    def delete(self, request, format=None, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'successful': True, 'data': {'message': 'Token removed successful.'}})


class TestView(APIView):
    def get(self, request, format=None):
        articles = ArticleSerializer(Article.objects.all(), many = True)
        return Response({'detail': "GET Response", 'objects' : articles.data})
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "user" not in data or "password" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=data["user"], password=data["password"])
        if not user:
            return Response('No default user, pleas create one', status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            token = Token.objects.get_or_create(user=user)
            return Response({'successful': True, 'detail': 'POST answer', 'token': token[0].key})
        else:
            return Response('Not enought permisson, just superuser can get this information', status=status.HTTP_401_UNAUTHORIZED)

class AccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        articles = ArticlesSerializer(article.objects.all(), many=True)
        return Response(data= series.data, status= status.HTTP_200_OK)
    def retrieve(self, request, pk: int):
        article = ArticlesSerializer(article.objects.get(pk= pk))
        return Response(data= series.data, status= status.HTTP_200_OK)
    def create(self, request):
        article = ArticlesSerializer(data = request.POST)
        article.is_valid(raise_exception= True)
        article.objects.create(title=article.validated_data['title'], description=article.validated_data['description'])
        return self.list(request)