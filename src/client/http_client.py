import requests
import threading
import json
import time
import queue

class Client:
    def __init__(self):
        self.lock = threading.Lock()
        self.request_queue = queue.Queue()
        self.delayed_requests = queue.Queue()
        self.stop_event = threading.Event()

        self._init_daemons()

    def terminate(self):
        self.stop_event.set()

    def _init_daemons(self):
        threading.Thread(target=self._delay_requests, daemon=True).start()
        threading.Thread(target=self._run_sync_requests, daemon=True).start()

    def _delay_requests(self):
        while not self.stop_event.is_set():
            self.stop_event.wait(1)
            if self.stop_event.is_set():
                break
            delayed_count = self.delayed_requests.qsize()
            for _ in range(delayed_count):
                request = self.delayed_requests.get(block=True)
                self.queue_sync_request(*request)

    def _run_sync_requests(self):
        # todo think about correct way to stop this thread
        # but it's not critical for now
        while True:
            request = self.request_queue.get(block=True)
            success, _ = self._send_sync_request(*request)
            if not success:
                self.delayed_requests.put(request)

    def _create_url(self, address):
        return f'http://{address}/map'

    def send_get_request(self, address):
        try:
            response = requests.get(self._create_url(address))
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            print(f"GET request failed: {e}")
            return False, None

    def send_patch_request(self, address, data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.patch(self._create_url(address), json=data, headers=headers)
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            print(f"PATCH request failed: {e}")
            return False, None

    def queue_sync_request(self, address, data, timestamp):
        self.request_queue.put((address, data, timestamp))

    def _send_sync_request(self, address, data, timestamp):
        try:
            headers = {'Content-Type': 'application/json'}
            params = {'timestamp': timestamp}
            response = requests.put(self._create_url(address), json=data, headers=headers, params=params)
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            print(f"PUT request failed: {e}")
            return False, None
