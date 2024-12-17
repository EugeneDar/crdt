import argparse
import time

from node.node import Node
from utils import cluster_info


def sleep_forever():
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--all',
        action='store_true'
    )
    parser.add_argument(
        '--node_id',
        type=str
    )
    parser.add_argument(
        '--cluster_size',
        type=int,
        default=1,
        help='Number of nodes in the cluster'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.all and args.node_id is not None:
        print("You can't use --all and --node_id together")
        return

    cluster_info.init_cluster_nodes(args.cluster_size)
    nodes = []

    if args.node_id is not None:
        nodes.append(Node(args.node_id))
        print(f"Node {args.node_id} started.")
        sleep_forever()
    elif args.all:
        print("Starting whole cluster...")
        nodes = [Node(node_id) for node_id in cluster_info.get_all_node_ids()]
        print("Cluster started.")
        sleep_forever()
    else:
        print("You need to specify --all or --node_id")
        return

    sleep_forever()


if __name__ == "__main__":
    main()
