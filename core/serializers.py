from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email',
                  'first_name', 'last_name', ]


class UserSerializer(BaseUserUserSerializer):
    class Meta(BaseUserUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name']
