
class TweetService:

    def __init__(self, model):
        from django.db.models.base import ModelBase
        if not isinstance(model, ModelBase):
            raise TypeError('model argument is not a django model')

        self.tweet_model = model

    def get_tweets_list(self):
        import random
        tweets = {'data': []}

        for t in self.tweet_model.objects.all():
            try:
                file_content_url = t.file_content.url
            except ValueError:
                file_content_url = None

            tweets['data'].append(
                    {
                        'id': t.id,
                        'content': t.text_content,
                        'file': file_content_url,
                        'likes': random.randint(1, 10_000_000)
                    }
                )
        return tweets
        

