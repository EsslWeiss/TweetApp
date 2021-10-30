from django import forms
from django.core.exceptions import ValidationError
from .models import Tweet

from django.urls import reverse
import ipdb


class TweetForm(forms.ModelForm):
    MAX_TWEET_LENGTH = 599

    class Meta:
        model = Tweet
        fields = ('text_content', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text_content'].widget.attrs.update(
                {
                    'id': 'textContentInput',
                    'required': 'required',
                    'placeholder': 'add your tweet today!'
                }
            )

    def clean_text_content(self):
        tweet = self.cleaned_data.get('text_content')
        if len(tweet) > self.MAX_TWEET_LENGTH:
            raise ValidationError('tweet length exceeded!')  # set error message to form.errors

        return tweet

