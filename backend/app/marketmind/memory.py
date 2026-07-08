class MemoryStore:
    def __init__(self): self.events = []
    def remember(self, event: dict):
        self.events.append(event)
        self.events = self.events[-100:]
    def recent(self, limit: int = 10): return self.events[-limit:]

memory_store = MemoryStore()
