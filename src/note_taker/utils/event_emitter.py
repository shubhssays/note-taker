from collections import defaultdict


class EventEmitter:
    def __init__(self):
        self.listeners = defaultdict(list)

    def on(self, event):
        def decorator(func):
            self.listeners[event].append(func)
            return func
        return decorator

    def emit(self, event, *args, **kwargs):
        for handler in self.listeners[event]:
            handler(*args, **kwargs)


