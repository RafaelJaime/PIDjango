from rest_framework import serializers
from account.models import User
from .models import Article, Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['first_name', 'last_name', 'username', 'first_name', 'last_name']

class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    latitude = serializers.DecimalField(max_digits = 30, decimal_places = 15)
    longitude = serializers.DecimalField(max_digits = 30, decimal_places = 15)
    telephone = serializers.DecimalField(max_digits = 30, decimal_places = 15)
    email = serializers.EmailField()
    startDate = serializers.DateField()
    endDate = serializers.DateField()
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    content = serializers.CharField()
    event = EventSerializer()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Article
        fields = ['__all__']

