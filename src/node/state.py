class State:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

    def update(self, new_value, new_timestamp):
        if self.timestamp.happens_before(new_timestamp):
            self.value = new_value
            self.timestamp = new_timestamp
            return True
        return False
