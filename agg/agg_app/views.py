import logging
import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.db import transaction
from celery.task import Task

from .misc import ArticleReq
from .misc import AuthorReq
from .misc import TopicReq
from .misc import AuthReq

from .task import ReqTask

logger = logging.getLogger('agg_logger')



class BaseView(View):
        article = ArticleReq('http://localhost:8005/')
        author = AuthorReq('http://localhost:8010/')
        topic = TopicReq('http://localhost:8015/')
        auth = AuthReq('http://localhost:8010/')

        def error_response(self, status, json_body):
            return HttpResponse(status=status,
                                content=json.dumps(json_body),
                                content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class OneArticleView(BaseView):

    #3
    # Вывести статью (с автором и темой)
    def get(self, request, article_id):
        context = {}
        error_message = request.GET.get('error_message')
        if error_message:
            if error_message == 'author_error':
                error_message = u'Сервис авторов недоступен, лайк автору будет поставлен позже'
            elif error_message == 'topic_error':
                error_message = u'Сервис тем недоступен, лайк теме будет поставлен позже'
            else:
                error_message = u'Ошибка с доступностью сервисов, ваше действие учтено и будет выполнено позднее'
        context['error_message'] = error_message
        try:
            if article_id == '0':
                status_code = 400
                context['status_code'] = status_code
                context['error_short'] = u"Неверно задан id статьи"
                return render(request, 'agg_app/error.html', context, status=status_code)
            try:
                article = self.article.get_one_json(article_id)
            except:
                status_code = 503
                context['status_code'] = status_code
                context['error_short'] = u"Сервис недоступен"
                return render(request, 'agg_app/error.html', context, status=status_code)

            error = article.get('detail')
            if error and error == 'Not found.':
                status_code = 404
                context['status_code'] = status_code
                context['error_short'] = u"Статья не найдена"
                return render(request, 'agg_app/error.html', context, status=status_code)

            author_id = article["author"]
            topic_id = article["topic"]

            try:
                author = self.author.get_one_json(author_id)
            except:
                author = article_id

            try:
                topic = self.topic.get_one_json(topic_id)
            except:
                topic = topic_id

            logger.info(u"Вывести статью с автором и темой")
            context['article'] = article
            context['author'] = author
            context['topic'] = topic
            return render(request, 'agg_app/detail.html', context)
        except:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            return render(request, 'agg_app/error.html', context, status=status_code)

    # Поставить лайк статье (увеличить лайки автора и темы)
    def post(self, request, article_id):
        context = {}
        try:
            if article_id == '0':
                status_code = 400
                context['status_code'] = status_code
                context['error_short'] = u"Неверно задан id статьи"
                return render(request, 'agg_app/error.html', context, status=status_code)

            if request.POST.get('like'):
                try:
                    article = self.article.get_one_json(article_id)
                except:

                    logger.info(u"Работа очереди")
                    ReqTask.delay("http://localhost:8000/agg/article/{0}/like/".format(article_id), "PATCH",article_id)

                    status_code = 503
                    context['status_code'] = status_code
                    context['error_short'] = u"Сервис недоступен"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                error = article.get('detail')

                if error and error == 'Not found.':
                    status_code = 404
                    context['status_code'] = status_code
                    context['error_short'] = u"Статья не найдена"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                author_id = article["author"]
                topic_id = article["topic"]

                try:
                    author = self.author.get_one_json(author_id)
                except:

                    logger.info(u"Работа очереди")
                    ReqTask.delay("http://localhost:8000/agg/article/{0}/like/".format(article_id), "PATCH", article_id)



                    r = HttpResponseRedirect(reverse('agg_app:article_one', kwargs={"article_id": article_id}))
                    error_message = 'author_error'
                    r['Location'] += "?error_message=%s" % error_message



                    return  r

                try:
                    topic = self.topic.get_one_json(topic_id)
                except:


                    logger.info(u"Работа очереди")
                    ReqTask.delay("http://localhost:8000/agg/article/{0}/like/".format(article_id), "PATCH",article_id)

                    r = HttpResponseRedirect(reverse('agg_app:article_one', kwargs={"article_id": article_id}))
                    error_message = 'topic_error'
                    r['Location'] += "?error_message=%s" % error_message

                    return r


                #доделать только здесь, остальное не трогать
                article_result = self.article.like(article_id)
                author_result = self.author.like(author_id)
                topic_result = self.topic.like(topic_id)




                result = {"article_result": article_result.status_code,
                          "author_result": author_result.status_code,
                          "topic_result": topic_result.status_code
                }

                logger.info(u"Поставить лайк статье (увеличить лайки автора и темы)")
                return HttpResponseRedirect(reverse('agg_app:article_one', kwargs={"article_id": article_id}))
            else:
                try:
                    article = self.article.get_one_json(article_id)
                except:
                    status_code = 503
                    context['status_code'] = status_code
                    context['error_short'] = u"Сервис статей недоступен"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                error = article.get('detail')
                if error and error == 'Not found.':
                    status_code = 404
                    context['status_code'] = status_code
                    context['error_short'] = u"Статья не найдена"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                author_id = article["author"]
                topic_id = article["topic"]

                try:
                    author_result = self.author.unlike(author_id)
                except:
                    status_code = 503
                    context['status_code'] = status_code
                    context['error_short'] = u"Сервис авторов недоступен"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                try:
                    topic_result = self.topic.unlike(topic_id)
                except:
                    author_result = self.author.like(author_id)
                    status_code = 503
                    context['status_code'] = status_code
                    context['error_short'] = u"Сервис тем недоступен"
                    return render(request, 'agg_app/error.html', context, status=status_code)

                article_result = self.article.delete_one(article_id)
                result = {"article_result": article_result.status_code,
                          "author_result": author_result.status_code,
                          "topic_result": topic_result.status_code
                          }
                logger.info(u"Удалить статью (удалить лайки у автора и темы)")
                return HttpResponseRedirect(reverse('agg_app:article_list'))
        except:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            return render(request, 'agg_app/error.html', context, status=status_code)



    #4
    # Удалить статью (удалить лайки у автора и темы)
    def delete(self, request, article_id):
        context = {}
        try:
            if article_id == '0':
                status_code = 400
                context['status_code'] = status_code
                context['error_short'] = u"Неверно задан id статьи"
                return render(request, 'agg_app/error.html', context, status=status_code)

            try:
                article = self.article.get_one_json(article_id)
            except:
                status_code = 503
                context['status_code'] = status_code
                context['error_short'] = u"Сервис статей недоступен"
                return render(request, 'agg_app/error.html', context, status=status_code)

            error = article.get('detail')
            if error and error == 'Not found.':
                status_code = 404
                context['status_code'] = status_code
                context['error_short'] = u"Статья не найдена"
                return render(request, 'agg_app/error.html', context, status=status_code)

            author_id = article["author"]
            topic_id = article["topic"]

            try:
                author_result = self.author.unlike(author_id)
            except:
                status_code = 503
                context['status_code'] = status_code
                context['error_short'] = u"Сервис авторов недоступен"
                return render(request, 'agg_app/error.html', context, status=status_code)

            try:
                topic_result = self.topic.unlike(topic_id)
            except:
                author_result = self.author.like(author_id)
                status_code = 503
                context['status_code'] = status_code
                context['error_short'] = u"Сервис тем недоступен"
                return render(request, 'agg_app/error.html', context, status=status_code)


            article_result = self.article.delete_one(article_id)
            result = {"article_result": article_result.status_code,
                            "author_result": author_result.status_code,
                            "topic_result": topic_result.status_code
                    }
            logger.info(u"Удалить статью (удалить лайки у автора и темы)")
            return HttpResponseRedirect(reverse('agg_app:article_list'))
        except:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            return render(request, 'agg_app/error.html', context, status=status_code)


class ListArticleView(BaseView):
    # Вывести статьи
    def get(self, request):
        context = {}
        try:
            self.article.get_list_all()
        except:
            status_code = 503
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            return render(request, 'agg_app/error.html', context, status=status_code)
        try:
            article_page = request.GET.get('article_page', '1')
            logger.info(u"Вывести статьи на заданную тему")
            response = self.article.get_list_all(article_page)
            if response.status_code == 200:
                response_json = response.json()
                article = response_json["results"]
                context['article'] = article
                context['article_page'] = article_page
                page_count = response_json['page_count']
                context['article_page_count'] = page_count
                context['article_page_range'] = range(1, page_count + 1)
                if response_json.get('previous'):
                    context['previous_page'] = int(article_page) - 1
                if response_json.get('next'):
                    context['next_page'] = int(article_page) + 1
            return render(request, 'agg_app/list.html', context)
        except:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            return render(request, 'agg_app/error.html', context, status=status_code)





@method_decorator(csrf_exempt, name='dispatch')
class TokenView(BaseView):
    def get(self, request):
        code = request.GET.get('code')
        print("Got authorization code:", code)
        print("Try to get access and refresh tokens")

        redirect_uri = 'http://localhost:8000/' + 'token/'

        access_token, refresh_token = self.auth.get_token_oauth(code, redirect_uri)
        print("Access token:", access_token)
        print("Refresh token:", refresh_token)

        response = HttpResponseRedirect(reverse('http://127.0.0.1:8000'))

        response.set_cookie('access_token', access_token, max_age=1800)
        response.set_cookie('refresh_token', refresh_token, max_age=1800)

        return response

@method_decorator(csrf_exempt, name='dispatch')
class AuthView(BaseView):
    def get(self, request):
        return HttpResponseRedirect(self.auth.create_authorization_link())








