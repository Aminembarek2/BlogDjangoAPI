from rest_framework import serializers
from articles.models import Post
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    )


class PostCreateUpdateSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'slug',
            'content',
            'created_date',
        ]

class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'created_date',
        ]

class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'content',
            'slug',
            'created_date',
        ]
        