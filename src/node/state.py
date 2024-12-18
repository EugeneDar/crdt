class State:
    def __init__(self, value, timestamp, source_id):
        self.value = value
        self.timestamp = timestamp
        self.source_id = source_id

    def update(self, new_value, new_timestamp, new_source_id):
        if self.timestamp < new_timestamp or (self.timestamp == new_timestamp and self.source_id < new_source_id):
            self.value = new_value
            self.timestamp = new_timestamp
            self.source_id = new_source_id
            return True
        return False
