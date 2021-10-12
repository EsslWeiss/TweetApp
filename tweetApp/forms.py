from django import forms
from .models import Tweet

from django.urls import reverse


class TweetForm(forms.Form):
    MAX_TWEET_LENGTH = 450

    text_content = forms.CharField(widget=forms.TextInput())
    redirect_to = forms.URLField(widget=forms.HiddenInput())

    class Meta:
        fields = ('text_content', 'redirect_to')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['redirect_to'].initial = reverse('tweetApp:tweets-list')

    def clean_text_content(self):
        tweet_text = self.cleaned_data.get('text_content')
        if len(tweet_text) > self.MAX_TWEET_LENGTH:
            raise self.ValidationError('tweet length exceeded')

        return tweet_text

