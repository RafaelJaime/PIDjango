from rest_framework import serializers
from account.models import User
from .models import Article, Event, Film, Character, Ranking, Post, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_newsPaperman', 'is_superuser', 'verified_email']


class EventSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = ['__all__']
        depth = 2


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


class ArticlesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(
        max_length=None, use_url=True
    )
    author = UserSerializer()
    # def validate(self, serie: Dict[str, str]):
    #     if not serie.get('title'):
    #         raise ValidationError('Title is mandatory')
    #     return serie

    class Meta:
        model = Article
        fields = '__all__'
        depth = 1

    def get_image_url(self, obj):
        return obj.image.url


class FilmsSerializer(serializers.ModelSerializer):
    # def validate(self, serie: Dict[str, str]):
    #     if not serie.get('title'):
    #         raise ValidationError('Title is mandatory')
    #     return serie

    class Meta:
        model = Film
        fields = '__all__'
        depth = 1


class CharactersSerializer(serializers.ModelSerializer):
    # def validate(self, serie: Dict[str, str]):
    #     if not serie.get('title'):
    #         raise ValidationError('Title is mandatory')
    #     return serie

    class Meta:
        model = Character
        fields = '__all__'
        depth = 1


class RankingSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Ranking
        fields = '__all__'
        depth = 2


class AnswersSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Answer
        fields = ['author', 'id', 'answer']
        depth = 2

class PostsSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_replies')

    def get_replies(self, obj):
        serializer = AnswersSerializer(Answer.objects.filter(post=obj.id), many=True,
                                       context={'request': self.context.get('request')})
        return serializer.data

    class Meta:
        model = Post
        fields = '__all__'
        depth = 1