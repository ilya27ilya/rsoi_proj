from rest_framework import viewsets
from rest_framework import pagination

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from topic_app.models import Topic
from topic_app.serializers import TopicSerializer


class TopicPagination(pagination.PageNumberPagination):
    page_size = 5


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = TopicPagination


@csrf_exempt
def like(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        topic.like_count += 1
        topic.save()
        serializer = TopicSerializer(topic)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"Error": "Method not allowed"})


@csrf_exempt
def unlike(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        topic.like_count -= 1
        topic.save()
        serializer = TopicSerializer(topic)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"Error": "Method not allowed"})
