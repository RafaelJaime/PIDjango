from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import viewsets

from .serializer import UserSerializer, ArticleSerializer, EventSerializer, ArticlesSerializer, FilmsSerializer, CharactersSerializer, RankingSerializer, PostsSerializer, AnswersSerializer

from account.models import User
from .models import Article, Event, Film, Character, Ranking, Post, Answer
# Emails
from account.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Create your views here.


@permission_classes([AllowAny])
class User_API(APIView):

    @permission_classes([IsAuthenticated])
    def get(self, request, format=None, *args, **kwargs):
        token = Token.objects.get_or_create(
            key=request.META.get('HTTP_AUTHORIZATION'))
        print(token)
        return Response({'successful': True, 'data': {'username': request.user.username, "is_staff": request.user.is_staff, "is_newsPaperman": request.user.is_newsPaperman}})

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

    @permission_classes([AllowAny])
    def put(self, request, format=None):
        user = User.objects.create_user(
            request.data['username'], password=request.data['password'], email=request.data['email'])
        if user:
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = request.data['email']
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return Response({'successful': True, 'data': {'username': request.data['username'], 'password': request.data['password']}})
        return Response({'successful': False, 'message': 'Bad credentials'})

    @permission_classes([IsAuthenticated])
    def delete(self, request, format=None, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'successful': True, 'data': {'message': 'Token removed successful.'}})


class TestView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        articles = ArticleSerializer(Article.objects.all(), many=True)
        return Response({'detail': "GET Response", 'objects': articles.data})

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
        if user:
            token = Token.objects.get_or_create(user=user)
            return Response({'successful': True, 'user': {"id": user.id, "username": user.username, "is_newsPaperman": user.is_newsPaperman, "is_superuser": user.is_superuser, "verified_email": user.verified_email}, 'token': token[0].key})
        else:
            return Response('Not enought permisson, just superuser can get this information', status=status.HTTP_401_UNAUTHORIZED)


class ArticleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        articles = ArticlesSerializer(
            Article.objects.order_by('-created_at'), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        article = ArticlesSerializer(Article.objects.get(pk=pk))
        return Response(data=series.data, status=status.HTTP_200_OK)

    def create(self, request):
        article = ArticlesSerializer(data=request.POST)
        article.is_valid(raise_exception=True)
        article.objects.create(
            title=article.validated_data['title'], description=article.validated_data['description'])
        return self.list(request)

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_200_OK)


class FilmViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        films = FilmsSerializer(Film.objects.all(), many=True)
        return Response(data=films.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        article = ArticlesSerializer(data=request.POST)
        article.is_valid(raise_exception=True)
        article.objects.create(
            title=article.validated_data['title'], description=article.validated_data['description'])
        return self.list(request)

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)


class CharacterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        characters = CharactersSerializer(Character.objects.all(), many=True)
        return Response(data=characters.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        article = ArticlesSerializer(data=request.POST)
        article.is_valid(raise_exception=True)
        article.objects.create(
            title=article.validated_data['title'], description=article.validated_data['description'])
        return self.list(request)

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)


class RankingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        rankings = RankingSerializer(Ranking.objects.filter(
            author=request.META.get('HTTP_ID')), many=True)
        return Response(data=rankings.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "rank" not in data or "film" not in data or "author" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        film = get_object_or_404(Film, id=data['film'])
        user = get_object_or_404(User, id=data['author'])
        d, created = Ranking.objects.get_or_create(
            film=film, author=user, defaults={'rank': data['rank']})
        d.rank = data['rank']
        d.save()
        return Response({"success": True})

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        posts = PostsSerializer(Post.objects.all(), many=True)
        return Response(data=posts.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "author" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(User, id=data['author'])
        post = Post(title=data['title'], author=user)
        post.save()
        return Response({"success": True})

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)


class AnswerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "post" not in data:
            return Response('Post required', status=status.HTTP_401_UNAUTHORIZED)
        user = Answer.objects.filter(post=data['post'])
        return Response(AnswersSerializer(user, many=True).data)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "answer" not in data or "post" not in data or "author" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, id=data['post'])
        user = get_object_or_404(User, id=data['author'])
        answer = Answer.objects.get_or_create(
            answer=data['answer'], post=post, author=user)
        return Response({"success": True})

    def update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        articles = ArticlesSerializer(Article.objects.all(), many=True)
        return Response(data=articles.data, status=status.HTTP_200_OK)
