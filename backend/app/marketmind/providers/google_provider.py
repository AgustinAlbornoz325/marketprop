import os

class GoogleProvider:
    name = "google"

    def available(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))

    def complete(self, task: dict) -> dict:
        return {
            "provider": self.name,
            "model": task.get("model", "gemini"),
            "mode": "gateway_ready",
            "message": "Gemini disponible por API key. Llamada real pendiente de activar."
        }
