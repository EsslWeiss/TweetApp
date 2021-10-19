from django.urls import path
from .views import *


app_name = 'tweetApp'
urlpatterns = [
    path('', TweetsHomePage.as_view(), name='tweets-homepage'),
    path('tweets/', TweetsListView.as_view(), name='tweets-list'),
    path('create-tweet/',  tweet_create_view, name='tweet-create')
]
