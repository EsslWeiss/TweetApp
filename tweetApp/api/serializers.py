from rest_framework import serializers
from django.conf import settings

from ..models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(required=False, format='%H:%M %d.%m.%y')

    class Meta:
        model = Tweet
        fields = ['text_content', 'date_created']
        extra_kwargs = {'text_content': {'required': True}}
     
    def validate_text_content(self, value):
        if len(value) > settings.MAX_TWEET_LENGTH:
            raise serializers.ValidationError('Your tweet is too long!')
        return value
 
