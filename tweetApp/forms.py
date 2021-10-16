from django import forms
from .models import Tweet

from django.urls import reverse
import ipdb


class TweetForm(forms.ModelForm):
    MAX_TWEET_LENGTH = 450

    to_next_page = forms.URLField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Tweet
        fields = ('text_content', )

    def __init__(self, *args, **kwargs):
        # kwargs = {'initial': {'to_next_page': 'url_to_next_page'}}
        super().__init__(*args, **kwargs)

    def clean_text_content(self):
        tweet = self.cleaned_data.get('text_content')
        if len(tweet) > self.MAX_TWEET_LENGTH:
            raise self.ValidationError('tweet length exceeded')

        return tweet

