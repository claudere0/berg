class EventBus:
    """
    A simple Event Bus (Publish/Subscribe) for decoupled communication between game entities.
    """
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type: str, listener: callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def emit(self, event_type: str, **kwargs):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(**kwargs)
