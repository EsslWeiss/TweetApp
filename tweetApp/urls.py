from django.urls import path, include
from .views import (
        tweets_homepage, tweets_list_view, 
        tweet_detail_view, tweet_create_view, 
        tweet_delete_view
    )
from .api import views as api_views 


api_urlpatterns = [
    path('tweets/', api_views.tweets_list_view, name='tweets-list'),
    path('tweet/<int:tweet_id>/detail', api_views.tweet_detail_view, name='tweet-detail'),
    path('tweet-create/', api_views.tweet_create_view, name='tweet-create'),
    path('tweet/<int:tweet_id>/delete', api_views.tweet_delete_view, name='tweet-delete'),
    path('tweet/action', api_views.tweet_action_view, name='tweet-action')
]

app_name = 'tweetApp'
urlpatterns = [
    path('', tweets_homepage, name='tweets-homepage'),
    # path('tweets/', tweets_list_view, name='tweets-list'),
    path('tweet/<int:tweet_id>/detail', tweet_detail_view, name='tweet-detail'),
    path('tweet-create/', tweet_create_view, name='tweet-create'),
    path('tweet/<int:tweet_id>/delete', tweet_delete_view, name='tweet-delete'),

    path('api/', include(api_urlpatterns))
]

