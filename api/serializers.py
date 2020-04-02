from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .models import Post, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
        )
        extra_kwargs = {
            'password':
                {
                    'write_only': True,
                    'required': True
                }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'created_at',
            'post',
            'user',
        )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'comments',
        )
