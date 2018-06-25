from multiprocessing import Process, Manager, Pool as ThreadPool
from threading import Thread
from time import time, sleep
import logging

class MultiThreader:
    def __init__(self):
        self.max_threads = 400
        self.queue = Manager().Queue(maxsize=0)
        self.active_threads = []
        self.inactive_threads = []

    def clear_queue(self):
        self.queue.clear()

    def clear_idle_threads(self):
        self.idle_threads = []

    def add_to_queue(self, item):
        try:
            self.queue.put(item)
        except Exception as e:
            logging.error('Unable to put item on queue:' + str(e))

    def get_from_queue(self):
        try:
            item = self.queue.get()
        except Exception as e:
            logging.error('Unable to retrieve item from queue: '+ str(e))
            item = None
        return item

    def add_thread(self, target, *args, **kwargs):
        try:
            thread = Thread(target=target, args=args, kwargs=kwargs)
            self.idle_threads.append(thread)
        except Exception as e:
            logging.error('Unable to create thread: ' + str (e))

    def run_threads(self, block_until_complete=False):
        for thread in self.idle_threads:
            self.run_thread(thread)
        if block_until_complete:
            self.join_threads()

    def switch_thread_to_active(self, thread):
        self.inactive_threads.remove(thread)
        self.active_threads.append(thread)

    def switch_thread_to_inactive(self, thread):
        self.inactive_threads.append(thread)
        self.active_threads.remove(thread)

    def run_thread(self, thread):
        try:
            thread.start()
        except Exception as e:
            logging.error('Unable to start thread' + str(e))

    def join_threads(self):
        try:
            for thread in self.threads:
                thread.join()
        except Exception as e:
            logging.error('Unable to join thread', + str(e))



