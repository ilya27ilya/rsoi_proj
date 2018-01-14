import requests
import datetime
from django.http import HttpResponse


CLIENT_ID = 'c9zxVoj3TEptwk5vldtc7EYaedcI6KlqYSXWq9bk'
CLIENT_SECRET = 'bZ9rEvC2rhd2Crhgl9SbGtHld7fub5w2KW8FUBOQ4Ii23iqDWjOK7VYWCvxPKygTsFKdwiKlLEQQ4fPJClBixZylEZNExLs24de7QoHMUtxFexrGARYoKK5Cc448TdIq'

CLIENT_ID_JSON = 'I4saB9ST0hELJTMSCu2SoG1z4r31BU7CacnA9zw6'
CLIENT_SECRET_JSON = 'jIaiNEUlySpGO4eSdU2FwRSBeZs0x1xmuPXnN39EKwCzgrUuZdCBIZOjP2Qaz23bBqZOR5rfuUNjELjqm1piKmnR3UHIrNYS7bmqOPtzq3p6kpl4VCyNbs1Nlmvyimoq'

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

    def patch(self, query_string, headers=None):
    #def patch(self, query_string, json, headers=None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers

        #r = requests.patch(self.host + query_string, json=json, headers=headers)
        r = requests.patch(self.host + query_string, headers=headers)
        if r.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            #r = requests.patch(self.host + query_string, json=json, headers=headers)
            r = requests.patch(self.host + query_string, headers=headers)
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

class AuthReq(BaseReq):
    def check_access_token(self, access_token):
        headers = {'Authorization': 'Bearer %s' % access_token}
        check = self.get('secret', headers=headers)
        return check.text == 'OK'

    def check_access_token_json(self, access_token):
        headers = {'Authorization': 'Bearer %s' % access_token}
        check = self.get('secret', headers=headers)
        return check.text == 'OK'

    def create_authorization_link(self):
        return self.host + 'o/authorize/?state=random_state_stringfgsfds&client_id=%s&response_type=code' % CLIENT_ID

    def create_authorization_link_json(self):
        return self.host + 'o/authorize/?state=random_state_stringfgsfds&client_id=%s&response_type=code' % CLIENT_ID_JSON

    def get_token_oauth(self, code, redirect_uri):
        post_json = {'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri}
        response = requests.post(self.host + 'o/token/', post_json, auth=(CLIENT_ID, CLIENT_SECRET))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')

    def get_token_oauth_json(self, code, redirect_uri):
        post_json = {'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri}
        response = requests.post(self.host + 'o/token/', post_json, auth=(CLIENT_ID_JSON, CLIENT_SECRET_JSON))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')

    def refresh_token(self, refresh_token):
        post_json = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        response = requests.post(self.host + 'o/token/', post_json, auth=(CLIENT_ID, CLIENT_SECRET))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')

    def refresh_token_json(self, refresh_token):
        post_json = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        response = requests.post(self.host + 'o/token/', post_json, auth=(CLIENT_ID_JSON, CLIENT_SECRET_JSON))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')




