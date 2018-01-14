import requests
import datetime
from django.http import HttpResponse


class BaseReq():
    def __init__(self, host, app_id='cska', app_secret='moscow'):
        self.host = host
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None


    def response_convert(self, requests_response):
        django_response = HttpResponse(
            content=requests_response.content,
            status=requests_response.status_code,
            content_type=requests_response.headers.get('Content-Type')
        )
        return django_response

    def get(self, query_string, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        r = requests.get(self.host + query_string, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            r = requests.get(self.host + query_string, headers=headers)
        return r

    def get_json(self, query_string, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        r = requests.get(self.host + query_string, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            r = requests.get(self.host + query_string, headers=headers)
        return r.json()

    def post(self, query_string, json, auth=None, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        r = requests.post(self.host + query_string, data=json, auth=auth, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            r = requests.post(self.host + query_string, data=json, auth=auth, headers=headers)
        return r

    def patch(self, query_string, json, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        r = requests.patch(self.host + query_string, json=json, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            r = requests.patch(self.host + query_string, json=json, headers=headers)
        return r

    def delete(self, query_string, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        r = requests.delete(self.host + query_string, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            r = requests.delete(self.host + query_string, headers=headers)
        return r

    def get_token(self):
        r = requests.post(self.host + "token/", {"username": self.app_id, "password": self.app_secret})
        r = r.json()
        self.token = r.get("token")

    @property
    def headers(self):
        return {"Authorization": "Token %s" % self.token}



class ArticleReq(BaseReq):

    def get_one_json(self, article_id):
        return self.get_json('article/%s/' % article_id)

    def like(self, article_id):
        return self.patch('like/%s/' % article_id)

    def delete_one(self, article_id):
        return self.delete('article/%s/' % article_id)

    def get_list_all(self, page=1):
        return self.get('article/?page=%s' % page)



class AuthorReq(BaseReq):
    def get_one_json(self, author_id):
        return self.get_json('author/%s/' % author_id)

    def like(self, author_id):
        return self.patch('like/%s/' % author_id)

    def unlike(self, author_id):
        return self.patch('unlike/%s/' % author_id)




class TopicReq(BaseReq):
    def get_one_json(self, topic_id):
        return self.get_json('topic/%s/' % topic_id)

    def like(self, topic_id):
        return self.patch('like/%s/' % topic_id)

    def unlike(self, topic_id):
        return self.patch('unlike/%s/' % topic_id)


