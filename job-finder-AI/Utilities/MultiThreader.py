from multiprocessing import Manager
from threading import Thread
import logging
from Utilities import QueueMonitor
from Utilities.ApplicationExceptions import MultiThreaderError
import traceback


class MultiThreader:
    def __init__(self):
        self.max_threads = 100
        self.queue = Manager().Queue(maxsize=0)
        self.active_threads = []
        self.inactive_threads = []
        self.monitor = None

    def run_queue_monitor(self, total):
        monitor = QueueMonitor.QueueMonitor(self.queue, total)
        self.monitor = Thread(target=monitor.run)
        self.monitor.start()

    def add_thread(self, *args, **kwargs):
        try:
            thread = Thread(target=self.wrap_thread, args=args, kwargs=kwargs)
            self.inactive_threads.append(thread)
        except Exception:
            raise MultiThreaderError('Unable to add thread to scheduler.')

    def wrap_thread(self, func, *args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logging.error('Error executing thread: ' + str(e))
            tb = traceback.format_exc()
            logging.error(tb)
        self.queue.put(result)

    def schedule_threads(self):
        thread_chunks = self.chunk_threads()
        for chunk in thread_chunks:
            self.run_threads(chunk)
        self.join_monitor()
        return self.queue

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
        self.inactive_threads.remove(thread)
        self.active_threads.append(thread)
        thread.start()

    @staticmethod
    def join_threads(chunk):
        try:
            for thread in chunk:
                thread.join()
        except Exception:
            raise MultiThreaderError('Unable to join threads.')

    def join_monitor(self):
        if self.monitor:
            self.monitor.join()

    def kill_active_threads(self):
        for thread in self.active_threads:
            self.kill_thread(thread)

    def kill_thread(self, thread):
        try:
            thread.stop()
            self.active_threads.remove(thread)
        except Exception:
            raise MultiThreaderError('Unable to kill thread.')

    def suspend_threads(self):
        for thread in self.active_threads:
            self.suspend_thread(thread)

    def suspend_thread(self, thread):
        try:
            thread.stop()
            self.inactive_threads.append(thread)
            self.active_threads.remove(thread)
        except Exception:
            raise MultiThreaderError('Unable to suspend thread.')

    def clear_queue(self):
        self.queue.clear()

    def clear_inactive_threads(self):
        self.inactive_threads = []
