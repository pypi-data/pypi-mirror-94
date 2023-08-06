class NotStringValueError(Exception):
    def __init__(self, value: str, pointer: str, resolved):
        super().__init__(f'only string types can be converted. value: [{value}] pointer: [{pointer}] resolved value: [{resolved}] resolved type: [{type(resolved)}]')
        self.value = value
        self.pointer = pointer
        self.resolved = resolved


class NotFoundError(Exception):
    def __init__(self, value, pointer):
        super().__init__(f'failed to find json pointer. value: [{value}] pointer: [{pointer}]')
        self.value = value
        self.pointer = pointer


class CircularReferenceError(Exception):
    def __init__(self, value):
        super().__init__(f'it is a circular reference. value: [{value}]')
        self.value = value
