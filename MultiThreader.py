from multiprocessing import Manager
from threading import Thread
import logging
import QueueMonitor


class MultiThreader:
    def __init__(self):
        self.max_threads = 400
        self.queue = Manager().Queue(maxsize=0)
        self.active_threads = []
        self.inactive_threads = []
        self.daemons = []

    def add_queue_monitor_thread(self, total):
        monitor = QueueMonitor.QueueMonitor(self.queue, total)
        self.add_thread(monitor.start)

    def run_daemon(self, target, *args, **kwargs):
        try:
            daemon = Thread(target=target, args=args, kwargs=kwargs)
            self.daemons.append(daemon)
            daemon.start()
        except Exception as e:
            logging.error('Error while adding daemon ' + str(e))

    def add_thread(self, *args, **kwargs):
        try:
            thread = Thread(target=self.wrap_thread, args=args, kwargs=kwargs)
            self.inactive_threads.append(thread)
        except Exception as e:
            logging.error('Unable to create thread: ' + str(e))

    def wrap_thread(self, func, *args, **kwargs):
        queue = self.queue
        result = func(*args, **kwargs)
        if result:
            queue.put(result)

    def schedule_threads(self):
        thread_chunks = self.chunk_threads()
        for chunk in thread_chunks:
            self.run_threads(chunk)

    def chunk_threads(self):
        chunk_size = self.max_threads
        chunks = [self.inactive_threads[i:i + chunk_size] for i in range(0, len(self.inactive_threads), chunk_size)]
        return chunks

    def run_threads(self, chunk, block_until_complete=True):
        for thread in chunk:
            self.run_thread(thread)
        if block_until_complete:
            self.join_threads(chunk)

    def run_thread(self, thread):
        try:
            self.inactive_threads.remove(thread)
            self.active_threads.append(thread)
            thread.start()
        except Exception as e:
            logging.error('Unable to start thread ' + str(e))

    @staticmethod
    def join_threads(chunk):
        try:
            for thread in chunk:
                thread.join()
        except Exception as e:
            logging.error('Unable to join thread ' + str(e))

    def join_daemon(self):
        for daemon in self.daemons:
            daemon.join()

    def kill_active_threads(self):
        for thread in self.active_threads:
            self.kill_thread(thread)

    def kill_thread(self, thread):
        try:
            thread.stop()
            self.active_threads.remove(thread)
        except Exception as e:
            logging.error('Unable to kill thread: ' + str (e))

    def suspend_threads(self):
        for thread in self.active_threads:
            self.suspend_thread(thread)

    def suspend_thread(self, thread):
        try:
            thread.stop()
            self.inactive_threads.append(thread)
            self.active_threads.remove(thread)
        except Exception as e:
            logging.error('Error while trying to suspend thread: ' + str(e))

    def clear_queue(self):
        self.queue.clear()

    def clear_inactive_threads(self):
        self.inactive_threads = []

    def add_to_queue(self, item):
        try:
            self.queue.put(item)
        except Exception as e:
            logging.error('Unable to put item on queue:' + str(e))

    def consume_queue(self):
        queue_items = []
        try:
            while not self.queue.empty():
                item = self.queue.get()
                queue_items.append(item)
        except Exception as e:
            logging.error('Error while consuming queue' + str(e))
        return queue_items

    def get_from_queue(self):
        item = None
        try:
            item = self.queue.get()
        except Exception as e:
            logging.error('Unable to retrieve item from queue: '+ str(e))
        return item
