import requests
import datetime
from django.http import HttpResponse


class BaseReq():
    def __init__(self, host):
        self.host = host

    def response_convert(self, requests_response):
        django_response = HttpResponse(
            content=requests_response.content,
            status=requests_response.status_code,
            content_type=requests_response.headers.get('Content-Type')
        )
        return django_response

    def get(self, query_string):
        r = requests.get(self.host + query_string)
        return r

    def get_json(self, query_string):
        r = requests.get(self.host + query_string)
        return r.json()

    def post(self, query_string, json):
        r = requests.post(self.host + query_string, json=json)
        return r

    def patch(self, query_string, json=None):
        r = requests.patch(self.host + query_string, json=json)
        return r

    def delete(self, query_string):
        r = requests.delete(self.host + query_string)
        return r


class ArticleReq(BaseReq):

    def get_one_json(self, article_id):
        return self.get_json('article/%s/' % article_id)

    def like(self, article_id):
        return self.patch('like/%s/' % article_id)

    def delete_one(self, article_id):
        return self.delete('article/%s/' % article_id)



    def post_one(self, author, text, topic):
        post_json = {'author': author, 'text': text, 'topic': topic}
        return self.post('article/', json=post_json)

    def get_list(self, topic_id, page=1):
        return self.get('article/?page=%s&topic=%s' % (page, topic_id))

    def get_list_all(self, page=1):
        return self.get('article/?page=%s' % page)



class AuthorReq(BaseReq):
    def get_one_json(self, author_id):
        return self.get_json('author/%s/' % author_id)

    def like(self, author_id):
        return self.patch('like/%s/' % author_id)

    def unlike(self, author_id):
        return self.patch('unlike/%s/' % author_id)

    def post_one(self, login, email, info):
        post_json = {'login': login, 'email': email, 'info': info}
        return self.post('author/', json=post_json)



class TopicReq(BaseReq):
    def get_one_json(self, topic_id):
        return self.get_json('topic/%s/' % topic_id)

    def like(self, topic_id):
        return self.patch('like/%s/' % topic_id)

    def unlike(self, topic_id):
        return self.patch('unlike/%s/' % topic_id)

    def post_one(self, title, info):
        post_json = {'title': title, 'info': info}
        return self.post('topic/', json=post_json)

