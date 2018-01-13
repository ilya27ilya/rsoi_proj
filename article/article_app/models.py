from django.db import models
import datetime


class Article(models.Model):
    author = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    text = models.TextField()
    topic = models.IntegerField(null=True)

