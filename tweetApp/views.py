from django.views.generic import View, ListView, DetailView 
from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.urls import reverse
from django.conf import settings

from .models import Tweet
from .forms import TweetForm
from .services import (TweetsCollection, TweetCreator)

import ipdb


class TweetsHomePage(View):
    template = 'tweetApp/pages/homepage.html' 
    form = TweetForm
    model = Tweet

    def get(self, request, *args, **kwargs):
        tweet_form = self.form(
                initial={'to_next_page': reverse('tweetApp:tweets-homepage')}
            )
        return render(
                request, 
                self.template,
                context={'tweet_form': tweet_form},
                status=200
            )

    def post(self, request, *args, **kwargs):
        to_next_page = request.POST['to_next_page']
        tweet_obj = TweetCreator(model=self.model)\
                .create_tweet(post_data=request.POST, form=self.form)
        if tweet_obj:
            tweet = TweetsCollection(model=Tweet).get_tweet_by_format(tweet_obj)
            return JsonResponse(tweet)


class TweetsListView(ListView):
    model = Tweet

    def get(self, request, *args, **kwargs):
        t_coll = TweetsCollection(model=self.model)
        t_list = t_coll.get_tweets_list()
        return JsonResponse(t_list)

