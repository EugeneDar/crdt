from flask import Flask, jsonify, request
import threading
from utils import cluster_info
from werkzeug.serving import make_server


class Server:
    def __init__(self, node):
        self.node = node
        self.port = cluster_info.get_port_by_node_id(node.id)
        self.local_app = Flask(__name__)
        self.server = None
        self.setup_routes()

    def terminate(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None

    def setup_routes(self):
        @self.local_app.route('/map', methods=['GET'])
        def get():
            self.node.logger.log('GET request received')
            result = self.node.handle_get()
            return jsonify(result), 200

        @self.local_app.route('/map', methods=['PATCH'])
        def patch():
            self.node.logger.log('PATCH request received')
            updates = request.get_json()
            self.node.handle_patch(updates)
            return jsonify({}), 202

        @self.local_app.route('/map', methods=['PUT'])
        def sync():
            self.node.logger.log('SYNC request received')
            updates = request.get_json()
            timestamp = request.args.get('timestamp')
            source_id = request.args.get('source_id')
            self.node.handle_sync(updates, timestamp, source_id)
            return jsonify({}), 202

    def run(self):
        self.node.logger.log(f'Starting server at address: localhost:{self.port}')
        self.server = make_server('localhost', self.port, self.local_app)
        self.server.serve_forever()
        self.node.logger.log(f'Server stopped at address: localhost:{self.port}')

    def run_as_daemon(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
