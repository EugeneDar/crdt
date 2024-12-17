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
    time.sleep(2)
    return nodes


def stop_all_nodes(nodes):
    for node in nodes:
        node.terminate()
    time.sleep(2)
    print("All nodes are stopped")


@pytest.mark.parametrize("nodes_count", [
    (1),
    (2), (3), (4),
    (5), (6), (7),
])
def test_nodes_rw(nodes_count):
    cluster_info.init_cluster_nodes(nodes_count)
    nodes = create_nodes()
    nodes_addresses = cluster_info.get_all_addresses()

    client = Client()

    client.send_patch_request(random.choice(nodes_addresses), {'key': 'a', 'value': 1})
    time.sleep(BROADCAST_TIME)
    success, response = client.send_get_request(random.choice(nodes_addresses))
    assert success
    assert response == {'key': 'a', 'value': 1}

    client.send_patch_request(random.choice(nodes_addresses), {'key2': 'b', 'value': 2})
    time.sleep(BROADCAST_TIME)
    success, response = client.send_get_request(random.choice(nodes_addresses))
    assert success
    assert response == {'key': 'a', 'key2': 'b', 'value': 2}

    stop_all_nodes(nodes)
