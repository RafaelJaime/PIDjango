from django.urls import include, path
from . import views

app_name='api'
urlpatterns = [
    path('token', views.TestView.as_view()),
    path('user', views.User_API.as_view()),
]