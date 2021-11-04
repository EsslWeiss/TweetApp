from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
            user,
            on_delete=models.CASCADE,
            related_name='tweets',
            related_query_name='tweets_query')
    text_content = models.TextField(blank=True, null=True)
    file_content = models.FileField(upload_to='files/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ['-date_created']

    def __str__(self):
        return "<%s: %s>" % (self.id, self.date_created)

