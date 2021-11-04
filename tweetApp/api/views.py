from ..models import Tweet

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (api_view, 
        permission_classes, 
        authentication_classes) 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TweetSerializer



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
    ipdb.set_trace()
    qs = Tweet.objects.filter(Q(id=tweet_id) & Q(user=request.user))
    if not qs.exists():
        return Response({'message': 'You cannot delete this tweet'}, status=404)
    
    tweet = qs.first()
    tweet.delete()
    return Response({'message': 'Tweet was deleted'}, status=200)

