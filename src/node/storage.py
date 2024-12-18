from .state import State


class Storage:
    def __init__(self):
        self.data = {}

    def get_all(self):
        return {key: state.value for key, state in self.data.items()}

    def put(self, key, value, timestamp, source_id):
        state = self.data.get(key)
        if state:
            state.update(value, timestamp, source_id)
        else:
            self.data[key] = State(value, timestamp, source_id)
