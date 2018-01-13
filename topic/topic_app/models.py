from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    like_count = models.IntegerField(default=0)