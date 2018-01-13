from rest_framework import serializers
from author_app.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'login', 'email', 'like_count', 'info')
