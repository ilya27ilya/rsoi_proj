import requests

from threading import Thread
from queue import Queue

storage = Queue()


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def do_work(self):
        if not storage.empty():
            urlData = storage.get()

            requests.post("http://localhost:8000/article/{0}/like/".format(urlData))
            #print("dfааа")

    def run(self):
        while not self.stopped.wait(2):
            self.do_work()


# this will stop the timer
# stopFlag.set()