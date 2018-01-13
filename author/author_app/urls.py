from django.conf.urls import url, include
from author_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'author', views.AuthorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^like/(?P<author_id>[0-9]+)/$', views.like),
    url(r'^unlike/(?P<author_id>[0-9]+)/$', views.unlike),
]
