from rest_framework import serializers
from django.conf import settings

from ..models import Tweet
from .bad_request_messages import (
        LONG_TWEET_MESSAGE, 
        WRONG_ACTION_FORMAT_MESSAGE, 
        ACTION_OPTION_NOT_DEFINED_MESSAGE,
        ACTION_ID_WAS_NEGATIVE_MESSAGE)
from django.contrib.auth import get_user_model

import ipdb


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    date_created = serializers.DateTimeField(required=False, format='%H:%M %d.%m.%y')

    class Meta:
        model = Tweet
        fields = ['id', 'text_content', 'date_created', 'likes']
        extra_kwargs = {'text_content': {'required': True}}

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_text_content(self, value):
        if len(value) > settings.MAX_TWEET_LENGTH:
            raise serializers.ValidationError(LONG_TWEET_MESSAGE)
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    date_created = serializers.DateTimeField(required=False, format='%H:%M %d.%m.%y')
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'text_content', 'date_created', 'likes']
        extra_kwargs = {'text_content': {'required': True}}

    def get_likes(self, obj):
        return obj.likes.count()

    def get_content(self, obj):
        return obj.content

    # def validate_text_content(self, value):
    #     if len(value) > settings.MAX_TWEET_LENGTH:
    #         raise serializers.ValidationError(LONG_TWEET_MESSAGE)
    #     return value


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        extra_kwargs = {'id': {'required': True}}
        extra_kwargs = {'action': {'required': True}}

    def validate_id(self, value):
        if value < 0:
            raise serializers.ValidationError(ACTION_ID_WAS_NEGATIVE_MESSAGE)
        return value
    
    def validate_action(self, value):
        if not isinstance(value, str): 
            raise serializers.ValidationError(WRONG_ACTION_FORMAT_MESSAGE)
        value = value.lower().strip()
        if value not in settings.TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError(ACTION_OPTION_NOT_DEFINED_MESSAGE)
        return value

