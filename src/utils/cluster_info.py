CLUSTER_NODES = {
    # '0': 'localhost:5030',
    # '1': 'localhost:5031',
    # '2': 'localhost:5032',
    # '3': 'localhost:5033',
    # '4': 'localhost:5034',
}

def init_cluster_nodes(nodes_count=3):
    global CLUSTER_NODES
    CLUSTER_NODES.clear()
    for i in range(nodes_count):
        node_id = str(i)
        CLUSTER_NODES[node_id] = f'localhost:{5030 + i}'


def get_node_address(node_id):
    return CLUSTER_NODES.get(node_id)


def get_node_id(address):
    for node_id, node_address in CLUSTER_NODES.items():
        if node_address == address:
            return node_id
    return None


def get_all_addresses():
    return list(CLUSTER_NODES.values())


def get_all_node_ids():
    return list(CLUSTER_NODES.keys())


def get_port_by_node_id(node_id):
    return int(get_node_address(node_id).split(':')[1])
