from time import sleep
import logging


class QueueMonitor:
    def __init__(self, queue, total):
        self.queue = queue
        self.total = total
        self.percent_complete = 0
        self.timeout_count_in_seconds = 600

    def start(self):
        current = 0
        count = 0
        while current < self.total and not self.is_timed_out(count):
            current = self.queue.qsize()
            self.percent_complete = round(current / self.total)
            logging.debug('Queue monitor: ' + str(current) + '/' + str(self.total))
            sleep(1)  # too slow - queue gets consumed and stuck here until timeout
            count += 1

    def is_timed_out(self, count):
        timed_out = count > self.timeout_count_in_seconds
        if timed_out:
            logging.error('Queue not consumed before timeout')
        return timed_out






