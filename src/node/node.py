import threading

from client.http_client import Client
from server.http_server import run_server_as_daemon, run_server
from .storage import Storage
from .timestamp import LamportTimestamp
from utils import cluster_info
from my_logger.logger import Logger


class Node:
    def __init__(self, id):
        self.id = id
        self.storage = Storage()
        # todo use vector clock
        self.timestamp = LamportTimestamp(0)
        self.http_client = Client()
        self.lock = threading.Lock()
        self.logger = Logger(id)

        run_server_as_daemon(cluster_info.get_port_by_node_id(id), self)
        # run_server(cluster_info.get_port_by_node_id(id), self)

    def handle_get(self):
        # self.logger.log('GET request received')
        with self.lock:
            return self.storage.get_all()

    def handle_patch(self, updates):
        # self.logger.log(f'PATCH request received')
        with self.lock:
            self.timestamp.increment()
            self.broadcast(updates, self.timestamp)

    def handle_sync(self, updates, timestamp):
        # self.logger.log(f'SYNC request received')
        timestamp = LamportTimestamp.from_string(timestamp)
        with self.lock:
            for key, value in updates.items():
                self.storage.put(key, value, timestamp)

    def broadcast(self, updates, timestamp):
        timestamp = timestamp.to_string()
        for address in cluster_info.get_all_addresses():
            self.logger.log(f'Sending updates to {address}')
            self.http_client.queue_sync_request(address, updates, timestamp)
