import requests
import logging

from celery.decorators import task
from celery.registry import tasks
from celery.task import Task

class ReqTask(Task):
    def __init__(self):
            logging.info('log ReqTask')

    def run(self, url, method, urlData):

        try:
            if (method == "PATCH"):

                logging.info(url)
                logging.info("celery work")

                r = requests.post("http://localhost:8000/article/{0}/like/".format(urlData))
                logging.info(r.status_code)




            else:
                requests.patch(url)

        except:
            logging.info("Error Celery")


tasks.register(ReqTask)