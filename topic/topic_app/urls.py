from django.conf.urls import url, include
from topic_app import views
from rest_framework.routers import DefaultRouter
from rest_framework_expiring_authtoken import views as l_views

router = DefaultRouter()
router.register(r'topic', views.TopicViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^like/(?P<topic_id>[0-9]+)/$', views.like),
    url(r'^unlike/(?P<topic_id>[0-9]+)/$', views.unlike),
    url(r'^token/', l_views.obtain_expiring_auth_token)
]
