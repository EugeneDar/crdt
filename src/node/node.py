import threading

from client.http_client import Client
from server.http_server import Server
from .storage import Storage
from .timestamp import LamportTimestamp
from utils import cluster_info
from my_logger.logger import Logger


class Node:
    def __init__(self, id):
        self.id = id
        self.storage = Storage()
        self.timestamp = LamportTimestamp()
        self.lock = threading.Lock()
        self.logger = Logger(id)
        self.http_client = Client()
        self.http_server = Server(self)

        self.http_server.run_as_daemon()

    def terminate(self):
        self.http_client.terminate()
        self.http_server.terminate()

    # for testing purposes
    def disable_sync(self):
        self.http_client.disable_sync()
        self.http_server.disable_sync()

    # for testing purposes
    def enable_sync(self):
        self.http_client.enable_sync()
        self.http_server.enable_sync()

    def handle_get(self):
        with self.lock:
            return self.storage.get_all()

    def handle_patch(self, updates):
        with self.lock:
            self.timestamp.increment()
            self.broadcast(updates, self.timestamp, self.id)
        self.handle_sync(updates, self.timestamp.to_string(), self.id)

    def handle_sync(self, updates, timestamp, source_id):
        timestamp = LamportTimestamp.from_string(timestamp)
        self.timestamp.update(timestamp)
        with self.lock:
            for key, value in updates.items():
                self.storage.put(key, value, timestamp, source_id)

    def broadcast(self, updates, timestamp, source_id):
        timestamp = timestamp.to_string()
        for address in cluster_info.get_all_addresses():
            if address == cluster_info.get_node_address(self.id):
                continue
            self.logger.log(f'Sending updates to {address}')
            self.http_client.queue_sync_request(address, updates, timestamp, source_id)
