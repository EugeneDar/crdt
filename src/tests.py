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


@pytest.mark.parametrize("patches_count,nodes_count", [
    (10, 3), (10, 10),
    (100, 3), (100, 10),
    (1000, 3), (1000, 10),
])
def test_many_patches(patches_count, nodes_count):
    cluster_info.init_cluster_nodes(nodes_count)
    nodes = create_nodes()
    nodes_addresses = cluster_info.get_all_addresses()

    client = Client()
    
    all_patches = [{f'key_{i}': f'value_{i}'} for i in range(patches_count)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for patch in all_patches:
            executor.submit(client.send_patch_request, random.choice(nodes_addresses), patch)

    wait_for_broadcast_time = max(1, patches_count * nodes_count / 100) * BROADCAST_TIME
    time.sleep(wait_for_broadcast_time)

    final_json = {f'key_{i}': f'value_{i}' for i in range(patches_count)}

    for node in nodes:
        success, response = client.send_get_request(cluster_info.get_node_address(node.id))
        assert success
        assert response == final_json

    stop_all_nodes(nodes)


@pytest.mark.parametrize("patches_count,nodes_count", [
    (10, 3), (10, 10),
    (100, 3), (100, 10),
    (1000, 3), (1000, 10),
])
def test_consistency(patches_count, nodes_count):
    cluster_info.init_cluster_nodes(nodes_count)
    nodes = create_nodes()
    nodes_addresses = cluster_info.get_all_addresses()

    clients = [Client() for _ in range(nodes_count)]

    def do_random_patches(client, patches_count, nodes_count):
        for _ in range(patches_count):
            random_patch = {
                f'key_{random.randint(0, nodes_count)}': f'value_{random.randint(0, nodes_count)}'
            }
            client.send_patch_request(random.choice(nodes_addresses), random_patch)

    with concurrent.futures.ThreadPoolExecutor(max_workers=nodes_count) as executor:
        for client in clients:
            executor.submit(do_random_patches, client, patches_count, nodes_count)

    # wait_for_broadcast_time = max(1, patches_count * nodes_count / 100) * BROADCAST_TIME
    wait_for_broadcast_time = max(1, patches_count * nodes_count / 30) * BROADCAST_TIME
    time.sleep(wait_for_broadcast_time)

    _, some_node_data = clients[0].send_get_request(random.choice(nodes_addresses))

    for address in nodes_addresses:
        _, node_data = clients[0].send_get_request(address)
        assert node_data == some_node_data

    stop_all_nodes(nodes)


def test_network_separation():
    # todo implement this test
    raise NotImplementedError
