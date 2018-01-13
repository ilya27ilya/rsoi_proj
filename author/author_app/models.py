from django.db import models


class Author(models.Model):
    login = models.CharField(max_length=30)
    email = models.EmailField()
    like_count = models.IntegerField(default=0)
    info = models.TextField()
