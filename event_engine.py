class EventEngine:
    def __init__(self):
        self._events = {}

    def register_event(self, event_name, callback):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback(*args, **kwargs)

    def remove_event(self, event_name, callback=None):
        if event_name in self._events:
            if callback:
                self._events[event_name].remove(callback)
            else:
                del self._events[event_name]

# Singleton instance
event_engine = EventEngine()