from django.urls import path
from .views import (TweetsHomePage, TweetsListView)


app_name = 'tweetApp'
urlpatterns = [
    path('', TweetsHomePage.as_view(), name='tweets-homepage'),
    path('tweets/', TweetsListView.as_view(), name='tweets-list'),
]
