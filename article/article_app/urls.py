from django.conf.urls import url, include
from article_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^like/(?P<article_id>[0-9]+)/$', views.like),
]
