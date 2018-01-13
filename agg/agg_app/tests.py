import requests_mock

from django.test import TestCase
from django.urls import reverse

from .misc import ARTICLE_URL
from .misc import AUTHOR_URL
from .misc import TOPIC_URL


@requests_mock.Mocker()
class ViewTests(TestCase):
    def test_article_get(self, m):
        article_id = 1
        author_id = 1
        topic_id = 1
        article_mock = {"author": author_id, "topic": topic_id}
        author_mock = {"author_answer": "OK"}
        topic_mock = {"topic_answer": "OK"}
        m.get(ARTICLE_URL + 'article/%s/' % article_id, json=article_mock)
        m.get(AUTHOR_URL + 'author/%s/' % author_id, json=author_mock)
        m.get(TOPIC_URL + 'topic/%s/' % topic_id, json=topic_mock)
        response = self.client.get(reverse('agg_app:article_one', kwargs={'article_id': article_id}))
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 3)
        self.assertEqual(response.json(), {"article": {"author": 1, "topic": 1}, "author": {"author_answer": "OK"},
                                           "topic": {"topic_answer": "OK"}})

    def test_article_like(self, m):
        article_id = 1
        author_id = 1
        topic_id = 1
        article_mock_get = {"author": author_id, "topic": topic_id}
        m.get(ARTICLE_URL + 'article/%s/' % article_id, json=article_mock_get)
        m.patch(ARTICLE_URL + 'like/%s/' % article_id)
        m.patch(AUTHOR_URL + 'like/%s/' % author_id)
        m.patch(TOPIC_URL + 'like/%s/' % topic_id)
        response = self.client.patch(reverse('agg_app:article_one', kwargs={'article_id': article_id}))
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 4)
        self.assertEqual(response.json(), {"article_result": 200, "author_result": 200, "topic_result": 200})

    def test_article_delete(self, m):
        article_id = 1
        author_id = 1
        topic_id = 1
        article_mock_get = {"author": author_id, "topic": topic_id}
        m.get(ARTICLE_URL + 'article/%s/' % article_id, json=article_mock_get)
        m.delete(ARTICLE_URL + 'article/%s/' % article_id, status_code=204)
        m.patch(AUTHOR_URL + 'unlike/%s/' % author_id)
        m.patch(TOPIC_URL + 'unlike/%s/' % topic_id)
        response = self.client.delete(reverse('agg_app:article_one', kwargs={'article_id': article_id}))
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 4)
        self.assertEqual(response.json(), {"article_result": 204, "author_result": 200, "topic_result": 200})


