from .state import State


class Storage:
    def __init__(self):
        self.data = {}

        # todo add field for not applied updates

    def get(self, key):
        state = self.data.get(key)
        return state.value, state.timestamp if state else None, None

    def get_all(self):
        return {key: state.value for key, state in self.data.items()}

    def put(self, key, value, timestamp):
        state = self.data.get(key)
        if state:
            state.update(value, timestamp)
        else:
            self.data[key] = State(value, timestamp)
