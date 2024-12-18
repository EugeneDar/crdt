class LamportTimestamp:
    def __init__(self, value=0):
        self.value = value

    def increment(self):
        self.value += 1
    
    def update(self, other):
        self.value = max(self.value, other.value) + 1

    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value

    def to_string(self):
        return str(self.value)

    @classmethod
    def from_string(cls, timestamp_str: str):
        value = int(timestamp_str)
        return cls(value)
