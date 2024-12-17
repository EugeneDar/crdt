class LamportTimestamp:
    def __init__(self, value: int):
        self.value = value

    def increment(self):
        self.value += 1
    
    def update(self, other):
        self.value = max(self.value, other.value) + 1

    def happens_before(self, other):
        return self.value < other.value
    
    def to_string(self):
        return str(self.value)

    @classmethod
    def from_string(cls, timestamp_str: str):
        value = int(timestamp_str)
        return cls(value)


# class VectorClocks:
#     def __init__(self, id: int):
#         self.id = id
#         self.value = {id: 0}

#     def increment(self):
#         self.value[self.id] += 1

#     def update(self, other):
#         for key in other.value:
#             self.value[key] = max(self.value.get(key, 0), other.value[key])

#     def happens_before(self, other):
#         if self.value[self.id] == other.value[self.id] + 1:
#             for key in self.value:
#                 if key != self.id:
#                     if self.value[key] > other.value[key]:
#                         return False
#             return True
#         return False
