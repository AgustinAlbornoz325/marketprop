import os

class AnthropicProvider:
    name = "anthropic"

    def available(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    def complete(self, task: dict) -> dict:
        return {
            "provider": self.name,
            "model": task.get("model", "claude-sonnet"),
            "mode": "gateway_ready",
            "message": "Claude disponible por API key. Llamada real pendiente de activar."
        }
