from rest_framework import viewsets
from rest_framework import pagination
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from author_app.models import Author
from author_app.serializers import AuthorSerializer


class AuthorPagination(pagination.PageNumberPagination):
    page_size = 5


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = AuthorPagination


@csrf_exempt
def like(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        author.like_count += 1
        author.save()
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"Error": "Method not allowed"})


@csrf_exempt
def unlike(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        author.like_count -= 1
        author.save()
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"Error": "Method not allowed"})
