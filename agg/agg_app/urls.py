from django.conf.urls import url

from . import views

app_name = 'agg_app'
urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/$', views.OneArticleView.as_view(), name='article_one'),
    url(r'^article/(?P<article_id>[0-9]+)/like/$', views.OneArticleView.as_view(), name='article_like'),
    url(r'^article/$', views.OneArticleView.as_view(), name='article_one'),
    url(r'^$', views.ListArticleView.as_view(), name='article_list'),

    url(r'^token/$', views.TokenView.as_view(), name='token'),
]
