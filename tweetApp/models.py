from django.db import models


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text_content = models.TextField(blank=True, null=True)
    file_content = models.FileField(upload_to='files/', blank=True, null=True)

