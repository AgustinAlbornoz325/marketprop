class MockProvider:
    name = "mock"
    def available(self) -> bool: return True
    def complete(self, task: dict) -> dict:
        return {"provider":self.name,"model":"marketmind-local-demo","mode":"demo","text":task.get("fallback_text", "MarketMind demo activo.")}
