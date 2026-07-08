import os

class OpenAIProvider:
    name = "openai"

    def available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    def complete(self, task: dict) -> dict:
        # v0.3.4: gateway preparado. La llamada real se conecta en el próximo sprint.
        return {
            "provider": self.name,
            "model": task.get("model", "gpt-5.5"),
            "mode": "gateway_ready",
            "message": "OpenAI disponible por API key. Llamada real pendiente de activar."
        }
