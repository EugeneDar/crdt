import copy
import pytest
import time
import sys
import random
import concurrent.futures

from utils import cluster_info
from node.node import Node
from client.http_client import Client
from utils.constants import *

def create_nodes():
    nodes = [Node(node_id) for node_id in cluster_info.get_all_node_ids()]
    time.sleep(3)  # todo use better way to wait for all nodes to start
    return nodes


def stop_all_nodes():
    time.sleep(7)  # todo use better way to wait for all nodes to stop


def test_one_node_rw():
    cluster_info.init_cluster_nodes(1)
    nodes = create_nodes()

    client = Client()

    client.send_patch_request(cluster_info.get_node_address('0'), {'key': 'a', 'value': 1})
    time.sleep(BROADCAST_TIME)
    success, response = client.send_get_request(cluster_info.get_node_address('0'))
    assert success
    assert response == {'key': 'a', 'value': 1}

    client.send_patch_request(cluster_info.get_node_address('0'), {'key2': 'b', 'value': 2})
    time.sleep(BROADCAST_TIME)
    success, response = client.send_get_request(cluster_info.get_node_address('0'))
    assert success
    assert response == {'key': 'a', 'key2': 'b', 'value': 2}

    stop_all_nodes()
