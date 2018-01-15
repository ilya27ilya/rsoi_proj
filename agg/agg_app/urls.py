from django.conf.urls import url

from . import views

app_name = 'agg_app'
urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/$', views.OneArticleView.as_view(), name='article_one'),
    url(r'^article/(?P<article_id>[0-9]+)/like/$', views.OneArticleView.as_view(), name='article_like'),
    url(r'^article/$', views.OneArticleView.as_view(), name='article_one'),
    url(r'^$', views.ListArticleView.as_view(), name='article_list'),

    url(r'^token/$', views.TokenView.as_view(), name='token'),
    url(r'^auth/$', views.AuthView.as_view(), name='auth'),

    url(r'^json/token/$', views.TokenViewJson.as_view(), name='token_json'),
    url(r'^json/auth/$', views.AuthViewJson.as_view(), name='auth_json'),

    url(r'^json/article/$', views.ListArticleViewJson.as_view(), name='article_list_json'),
    url(r'^json/article/(?P<article_id>[0-9]+)/like/$', views.OneArticleViewJson.as_view(), name='article_like'),

]
