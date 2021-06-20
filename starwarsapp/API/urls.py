from django.urls import include, path
from . import views

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'api'
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token', views.TestView.as_view()),
    path('user', views.User_API.as_view()),
    path('articles', views.ArticleViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('films', views.FilmViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('characters', views.CharacterViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('ranking', views.RankingViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('forum', views.PostViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('answer', views.AnswerViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('event', views.EventViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('joinevent', views.EventView.as_view()),
]
