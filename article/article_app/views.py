from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from article_app.models import Article
from article_app.serializers import ArticleSerializer

from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication#
from rest_framework.permissions import IsAuthenticated#
from django.contrib.auth.models import User#
from rest_framework.authtoken.models import Token#

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


class ArticlePagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page_count': self.page.paginator.num_pages,
        })


class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('topic',)



@csrf_exempt
def like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        article.like_count += 1
        article.save()
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"Error": "Method not allowed"})
