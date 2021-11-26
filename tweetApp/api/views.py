from ..models import Tweet
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (api_view, 
        permission_classes, 
        authentication_classes) 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (TweetSerializer, TweetCreateSerializer, TweetActionSerializer, RetweetSerializer)

import ipdb

@api_view(['GET']) # К контроллеру можно получить доступ только с помощью http метода GET
def tweets_list_view(request, *args, **kwargs):
    # Вывод списка твитов
    qs = Tweet.objects.all()
    serial = TweetSerializer(qs, many=True) # Сериализация объекта твитов в примитивный тип Python
    return Response(serial.data, status=200)  # Возвращает JSON с данными и статусом 200 - запрос выполнен успешно
    

@api_view(['GET']) # К контроллеру можно получить доступ только с помощью http метода GET
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    # Вывод детальной информации о твите
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        # Если твит не найден - возвращаем информацио об ошибке в JSON формате
        return Response({'message': 'tweet not found'}, status=404)

    tweet_obj = qs.first()
    serial = TweetSerializer(tweet_obj) # Сериализация конкретного объекта твита в примитивный тип Python
    return Response(serial.data, status=200) # Возвращает JSON с данными и статусом 200 - запрос выполнен успешно


@api_view(['POST']) # К контроллеру можно получить доступ только с помощью http метода POST
@permission_classes([IsAuthenticated]) # Не аутентифицированный пользователь не может получить доступ к контроллеру
# Будет возвращён http код 403 - пользователь не аутентифицирован
def tweet_create_view(request, *args, **kwargs):
    '''
        Контроллер создания твита:
            - Поддерживает только метод HTTP POST
            - Не аутентифицированные пользователи создавать твиты не могут
            - Поддержка AJAX запросов
            - Используем TweetCreateSerializer для создания объекта твита
    '''
    serial = TweetCreateSerializer(data=request.POST or None) # Заполняем сериализатор данными, которые пришли в HTTP body
    if serial.is_valid(): # Проверка данных полей сериализатора на валидность
        tweet_obj = serial.save(user=request.user) # Создаём новый объект твита, указываем отправившего твит пользователя.
        if request.is_ajax():
            serial = TweetSerializer(tweet_obj)
            return Response(serial.data, status=201) # Возвращает JSON с данными и статусом 201 - успешно создан новый объект
    if serial.errors: # Данные полей сериализатора не вылидны. Проверяем наличие ошибок
        if request.is_ajax():
            return Response({'error_messages': serial.errors}, status=400) # Возвращаем информацию об ошибе.

    return Response({}, status=404) # Поведение не обработано...


@api_view(['DELETE', 'POST']) # К контроллеру можно получить доступ только с помощью http метода DELETE и POST
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, *args, **kwargs):
    '''
        Контроллер удаления твита:
            - Контроллер получает HTTP body 'id=xxx'
            - id - обязательный параметр
    '''
    ipdb.set_trace()
    tweet_id = request.POST.get('id')
    qs = Tweet.objects.filter(Q(id=int(tweet_id)) & Q(user=request.user))
    if not qs.exists():
        return Response({'message': 'You cannot delete this tweet'}, status=400)
    
    tweet = qs.first()
    tweet.delete()
    return Response({'message': 'Tweet was deleted'}, status=200)


@api_view(['POST']) # К контроллеру можно получить доступ только с помощью http метода DELETE и POST
@permission_classes([IsAuthenticated]) 
def tweet_action_view(request, *args, **kwargs):
    '''
        Контроллер обработки действий над твитом.
            - Контроллер получает HTTP body 'id=xxx&action=yyy&content=zzz'
            - id - обязательный параметр
            - Действия над твитом: like, unlike, retweet
    '''
    ipdb.set_trace()
    action_serial = TweetActionSerializer(data=request.data) # Заполняем сериализатор данными, которые пришли в HTTP body
    if action_serial.is_valid(): # Проверка данных полей сериализатора на валидность
        data = action_serial.validated_data # Получаем проверенные данные 
        tweet_id = data.get('id')
        tweet_action = data.get('action')
        tweet_content = data.get('content')
        qs = Tweet.objects.filter(id=tweet_id)

        if not qs.exists():
            # Твит не найден! возвращаем информацию об ошибке со статусом 404 - ресурс не найден.
            return Response({'message': 'Sorry, something went wrong!'}, status=404)
        tweet = qs.first()
        if tweet_action == 'like':
            tweet.likes.add(request.user) # К твиту добавляем лайк от отправившего запрос пользователя
            tweet_serial = TweetSerializer(tweet) # Сериализуем объект твита в примитивный тип Python
        
        elif tweet_action == 'unlike':
            tweet.likes.remove(request.user) # Убираем лайк пользователя
            tweet_serial = TweetSerializer(tweet) # Сериализуем объект твита в примитивный тип Python

        elif tweet_action == 'retweet':
            parent_tweet = tweet
            new_tweet = Tweet.objects.create(
                    text_content=tweet_content,
                    user=request.user, 
                    parent=parent_tweet)
            tweet_serial = TweetSerializer(new_tweet)
    
    if action_serial.errors: # Если поля сериализатора не валидны - возвращаем сообщение об ошибке с кодом 400 - запрос не обработан
        return Response({'message': action_serial.errors}, status=400)
    
    return Response(tweet_serial.data, status=200)  # Поведение не обработано...

