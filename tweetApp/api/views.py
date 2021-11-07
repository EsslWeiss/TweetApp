from ..models import Tweet

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (api_view, 
        permission_classes, 
        authentication_classes) 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (TweetSerializer, TweetActionSerializer)

import ipdb

@api_view(['GET'])
def tweets_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serial = TweetSerializer(qs, many=True)
    return Response(serial.data, status=200)
    

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({'message': 'tweet not found'}, status=404)

    tweet_obj = qs.first()
    serial = TweetSerializer(tweet_obj)
    return Response(serial.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def tweet_create_view(request, *args, **kwargs):
    serial = TweetSerializer(data=request.POST or None)
    if serial.is_valid():
        serial.save(user=request.user)
        if request.is_ajax():
            return Response(serial.data, status=201)
    if serial.errors:
        if request.is_ajax():
            return Response({'error_messages': serial.errors}, status=400)

    return Response({}, status=404)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(Q(id=tweet_id) & Q(user=request.user))
    if not qs.exists():
        return Response({'message': 'You cannot delete this tweet'}, status=404)
    
    tweet = qs.first()
    tweet.delete()
    return Response({'message': 'Tweet was deleted'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def tweet_action_view(request, *args, **kwargs):
    '''
        id is required params in HTTP body
        action options: like, unlike, retweet
    '''
    ipdb.set_trace()
    serial = TweetActionSerializer(data=request.data)
    if serial.is_valid():
        data = serial.validated_data
        tweet_id = data.get('id')
        tweet_action = data.get('action')
        tweet_content = data.get('content')
        qs = Tweet.objects.filter(id=tweet_id)

        if not qs.exists():
            return Response({'message': 'Sorry, something went wrong!'}, status=404)
        tweet = qs.first()
        if tweet_action == 'like':
            tweet.likes.add(request.user)
            serial = TweetSerializer(tweet)
            return Response(serial.data, status=200)
        
        elif tweet_action == 'unlike':
            tweet.likes.remove(request.user)
        
        elif tweet_action == 'retweet':
            parent_tweet = tweet
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=parent_tweet,
                    text_content=tweet_content)
            serial = TweetSerializer(new_tweet)
            return Response(serial.data, status=200)
    
    if serial.errors:
        return Response({'message': serial.errors}, status=400)
    
    return Response(serializer, status=200)

