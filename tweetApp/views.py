from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse

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
    tweet_form = TweetForm(request.POST or None)
    if tweet_form.is_valid():
        tweet_obj = tweet_form.save(commit=False)
        tweet_obj.save()
        tweet_form = TweetForm(instance=tweet_obj)

    context = {'tweet_form': tweet_form}
    return render(request, 
            'tweetApp/pages/components/create_tweet_form.html', 
            context)

