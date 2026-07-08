from app.marketmind.providers.registry import provider_registry

class ModelRouter:
    """
    Decide qué proveedor/modelo conviene para cada tarea.
    En v0.3.4 ya detecta API keys y deja preparado el gateway multi-modelo.
    """

    def choose_model(self, task_type: str, platform: str | None = None) -> dict:
        available = provider_registry.available()

        # Reglas iniciales de MarketMind. En producción se reemplazan por métricas reales.
        if platform == "tiktok" and available.get("anthropic"):
            return {"provider": "anthropic", "model": "claude-sonnet", "reason": "razonamiento y guiones"}
        if platform == "meta_ads" and available.get("openai"):
            return {"provider": "openai", "model": "gpt-5.5", "reason": "copy corto y performance ads"}
        if task_type == "evaluation" and available.get("openai"):
            return {"provider": "openai", "model": "gpt-5.5", "reason": "evaluación estructurada"}
        if platform in ["instagram", "facebook"] and available.get("anthropic"):
            return {"provider": "anthropic", "model": "claude-sonnet", "reason": "redacción natural"}
        if available.get("google"):
            return {"provider": "google", "model": "gemini", "reason": "fallback multimodal futuro"}

        return {"provider": "mock", "model": "marketmind-local-demo", "reason": "sin API keys, modo local"}

    def provider_status(self) -> dict:
        return provider_registry.available()
