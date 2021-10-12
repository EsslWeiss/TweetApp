from django.urls import path
from .views import *


app_name = 'tweetApp'
urlpatterns = [
    path('', homepage, name='homepage'),
    path('tweets/', tweets_list_view, name='tweets-list'),
    path('create-tweet/',  tweet_create_view, name='tweet-create')
]
