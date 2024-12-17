import threading
from datetime import datetime


lock = threading.Lock()


class Logger:
    def __init__(self, node_id=None):
        self.node_id = node_id

    def log(self, text):
        now = datetime.now()
        formatted_time = '(' + now.strftime("%H:%M:%S.%f")[:-3] + ') '
        with lock:
            if self.node_id:
                print(formatted_time + f'[Node {self.node_id}]: ' + text)
            else:
                print(formatted_time + text)
