from time import sleep, time
import logging


class QueueMonitor:
    def __init__(self, queue, total_size):
        self.queue = queue
        self.total_size = total_size
        self.max_stale_time = 30

    def run(self):
        current_size = self.queue.qsize()
        last_update_time = time()
        while current_size < self.total_size and not self.is_queue_stale(last_update_time):
            previous_size = current_size
            current_size = self.queue.qsize()
            last_update_time = self.get_last_update_time(last_update_time, previous_size, current_size)
            logging.debug('Queue status: ' + str(current_size) + '/' + str(self.total_size))
            sleep(1)

    @staticmethod
    def get_last_update_time(last_update_time, previous_size, current_size):
        if current_size > previous_size:
            last_update_time = time()
        return last_update_time

    def is_queue_stale(self, last_update_time):
        current_time = time()
        current_stale_time = int(current_time - last_update_time)
        is_stale = current_stale_time > self.max_stale_time
        if is_stale:
            logging.error('Queue is stale for ' + str(current_stale_time) + 'seconds')
        return is_stale














