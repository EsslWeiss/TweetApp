from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.urls import reverse
from django.conf import settings

from .models import Tweet
from .forms import TweetForm

import ipdb


def homepage(request, *args, **kwargs):
    return render(request, 'tweetApp/pages/homepage.html', status=200)


def tweets_list_view(request, *args, **kwargs):
    import random
    tweets = {'data': []}
    for t in Tweet.objects.all():
        try:
            f = t.file_content.url
        except ValueError:
            f = None

        tweets['data'].append(
                {
                    'id': t.id,
                    'content': t.text_content,
                    'file': f,
                    'likes': random.randint(0, 1000)
                }
            )
    return JsonResponse(tweets)


def tweet_create_view(request, *args, **kwargs):
    ipdb.set_trace()
    if request.method == "POST":
        to_next_page = request.POST['to_next_page']
        tweet_form = TweetForm({'text_content': request.POST['text_content']})

        if tweet_form.is_valid():
            tweet_obj = tweet_form.save(commit=False)
            tweet_obj.save()
            if is_safe_url(to_next_page, settings.ALLOWED_HOSTS):
                return redirect(to_next_page)

            return redirect(reverse('tweetApp:tweets-list'))
    else:
        tweet_form = TweetForm(initial={'to_next_page': reverse('tweetApp:tweets-list')})

    return render(request,
        'tweetApp/pages/components/create_tweet_form.html', 
        {'tweet_form': tweet_form})

