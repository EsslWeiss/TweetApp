from django.views.generic import View, ListView, DetailView 
from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.urls import reverse
from django.conf import settings

from .models import Tweet
from .forms import TweetForm
from .services import TweetService

import ipdb


class TweetsHomePage(View):
    template = 'tweetApp/pages/homepage.html' 
    form = TweetForm

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
        tweet_form = self.form({'text_content': request.POST['text_content']})
        if tweet_form.is_valid():
            tweet_obj = tweet_form.save(commit=False)
            tweet_obj.save()
            if is_safe_url(to_next_page, settings.ALLOWED_HOSTS):
                return redirect(to_next_page, status=200)
            
            return redirect(reverse('tweetApp:tweets-homepage'))


class TweetsListView(ListView):
    model = Tweet

    def get(self, request, *args, **kwargs):
        t_serv = TweetService(model=self.model)
        tweets_list = t_serv.get_tweets_list()
        return JsonResponse(tweets_list)

