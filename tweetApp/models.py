from django.db import models


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text_content = models.TextField(blank=True, null=True)
    file_content = models.FileField(upload_to='files/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ['-date_created']

    def __str__(self):
        return "<[%s, %s]: %s>" % (self.id, self.text_content, self.date_created)

