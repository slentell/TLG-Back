from rest_framework import serializers
from djoser.conf import settings as djoser_settings
from stream_chat import StreamChat
from django.conf import settings
from djoser.serializers import UserCreateSerializer, TokenSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'account_type', 'profile_picture')
        

class StreamTokenSerializer(TokenSerializer):
    stream_token = serializers.SerializerMethodField()

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ('auth_token','stream_token')

    def get_stream_token(self, obj):
        client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)
        token = client.create_token(obj.user.id)
        print('get stream token return token ', token)
        return token