from django.views.generic import View, ListView, DetailView 
from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.urls import reverse_lazy
from django.conf import settings

from .models import Tweet
from .forms import TweetForm
from .services import (TweetsCollection, TweetCreator)

import ipdb


class TweetsHomePage(View):
    template = 'tweetApp/pages/homepage.html' 
    form = TweetForm
    model = Tweet
    to_next_page = reverse_lazy('tweetApp:tweets-homepage')

    def not_ajax_request(self, request, is_valid, form=None):
        if is_valid:
            return redirect(self.to_next_page)
        else:
            # else form is invalid. return form with errors.
            return render(
                    request, 
                    self.template, 
                    context={'tweet_form': form},
                    status=200
                )

    def get(self, request, *args, **kwargs):
        tweet_form = self.form()
        return render(
                request, 
                self.template,
                context={'tweet_form': tweet_form},
                status=200
            )

    def post(self, request, *args, **kwargs):
        response = TweetCreator(model=self.model)\
                .create_tweet(post_data=request.POST, form=self.form)
        if response.is_valid:
            tweet = TweetsCollection(model=self.model)\
                    .get_tweet_by_format(response.object)
            if request.is_ajax():
                return JsonResponse(tweet, status=201)
        if response.errors:
            if request.is_ajax():
                return JsonResponse(response.errors, status=400)
        
        return self.not_ajax_request(
                request, 
                is_valid=response.is_valid, 
                form=response.form
            )


class TweetsListView(ListView):
    model = Tweet

    def get(self, request, *args, **kwargs):
        t_coll = TweetsCollection(model=self.model)
        t_list = t_coll.get_tweets_list()
        return JsonResponse(t_list)

