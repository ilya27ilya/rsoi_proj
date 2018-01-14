from django.conf.urls import url, include
from article_app import views
from rest_framework.routers import DefaultRouter
from rest_framework_expiring_authtoken import views as l_views

router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^like/(?P<article_id>[0-9]+)/$', views.like),
    url(r'^token/', l_views.obtain_expiring_auth_token)
]
