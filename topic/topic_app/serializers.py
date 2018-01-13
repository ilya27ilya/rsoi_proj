from rest_framework import serializers
from topic_app.models import Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'info', 'like_count')
