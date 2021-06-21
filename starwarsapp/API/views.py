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
        pass
    
    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "subtitle" not in data or "content" not in data or "author" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(User, id=data['author'])
        character = Article.objects.create(title=data['title'], subtitle= data['subtitle'], content = data['content'], author = user)
        character.save()
        return Response({"success": True})

    def update(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "subtitle" not in data or "content" not in data or "id" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        article = get_object_or_404(Article, id=data['id'])
        article.title = data['title']
        article.subtitle = data['subtitle']
        article.content = data['content']
        article.save()
        return Response({"success": True})

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Article.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class FilmViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        films = FilmsSerializer(Film.objects.all(), many=True)
        return Response(data=films.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "director" not in data or "producer" not in data or "sipnosis" not in data or "release_date" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        character = Film.objects.create(title=data['title'], director= data['director'], producer = data['producer'], sipnosis = data['sipnosis'], release_date = data['release_date'])
        character.save()
        return Response({"success": True})

    def update(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "director" not in data or "producer" not in data or "sipnosis" not in data or "release_date" not in data or "id" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        film = get_object_or_404(Film, id=data['id'])
        film.title = data['title']
        film.director = data['director']
        film.producer = data['producer']
        film.sipnosis = data['sipnosis']
        film.release_date = data['release_date']
        film.save()
        return Response({"success": True})

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Film.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class CharacterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        characters = CharactersSerializer(Character.objects.all(), many=True)
        return Response(data=characters.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "name" not in data or "actor" not in data or "biography" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        character = Character.objects.create(name=data['name'], actor= data['actor'], biography = data['biography'])
        character.save()
        return Response({"success": True})

    def update(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "name" not in data or "actor" not in data or "biography" not in data or "id" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        character = get_object_or_404(Character, id=data['id'])
        character.name = data['name']
        character.actor = data['actor']
        character.biography = data['biography']
        character.save()
        return Response({"success": True})

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Character.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


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
        pass

    def partial_update(self, request):
        pass

    def destroy(self, request):
        pass


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
        pass

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Post.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


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
        pass

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Answer.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

class EventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        print(EventSerializer(Event.objects.all(), many=True).data)
        posts = EventSerializer(Event.objects.all(), many=True)
        return Response(data=posts.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk: int):
        pass

    def create(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "title" not in data or "telephone" not in data or "email" not in data or "startDate" not in data or "endDate" not in data or "article" not in data:
            return Response('fields required', status=status.HTTP_401_UNAUTHORIZED)
        article = get_object_or_404(Article, id=data['article'])
        event = Event.objects.create(title = data['title'], telephone = data['telephone'], email = data['email'], startDate = data['startDate'], endDate = data['endDate'])
        event.save()
        article.event = event
        article.save()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def update(self, request):
        pass

    def partial_update(self, request):
        pass

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "id" not in data :
            return Response('ID needed', status=status.HTTP_401_UNAUTHORIZED)
        article = Answer.objects.get(id=data["id"])
        article.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

class EventView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaled JSON - {0}'.format(error.detail), status=status.HTTP_404_NOT_FOUND)
        if "user" not in data or "event" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        event = get_object_or_404(Event, id=data['event'])
        user = get_object_or_404(User, id=data['user'])
        print(event.id)
        print(user.id)
        if user in event.participants.all():
            event.participants.remove(user)
        else:
            event.participants.add(user)
        return Response({"success": True}, status=status.HTTP_200_OK)