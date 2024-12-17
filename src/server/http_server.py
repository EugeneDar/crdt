from flask import Flask, jsonify, request
import threading


def run_server(port, node):
    local_app = Flask(__name__)

    @local_app.route('/map', methods=['GET'])
    def get():
        node.logger.log('GET request received')
        result = node.handle_get()
        return jsonify(result), 200

    @local_app.route('/map', methods=['PATCH'])
    def patch():
        node.logger.log('PATCH request received')
        updates = request.get_json()
        node.handle_patch(updates)
        return jsonify({}), 202

    @local_app.route('/map', methods=['PUT'])
    def sync():
        node.logger.log('SYNC request received')
        updates = request.get_json()
        timestamp = request.args.get('timestamp')
        node.handle_sync(updates, timestamp)
        return jsonify({}), 202

    print(f'Starting server at address: localhost:{port}')
    local_app.run(port=port, debug=False)


def run_server_as_daemon(port, node):
    threading.Thread(target=run_server, args=(port, node), daemon=True).start()
