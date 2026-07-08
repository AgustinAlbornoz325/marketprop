class MockProvider:
    name = "mock"

    def available(self) -> bool:
        return True

    def complete(self, task: dict) -> dict:
        return {
            "provider": self.name,
            "model": task.get("model", "marketmind-mock"),
            "mode": "local_demo",
            "message": "Proveedor mock activo. La app funciona sin API keys."
        }
