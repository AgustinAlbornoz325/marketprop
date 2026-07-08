class ModelRouter:
    """En producción decide entre GPT, Claude, Gemini u otros. En v0.3.3 usa modo mock."""
    def choose_model(self, task_type: str, platform: str | None = None) -> dict:
        if task_type == "evaluation": return {"provider":"mock", "model":"marketmind-evaluator"}
        if platform == "tiktok": return {"provider":"mock", "model":"marketmind-video-copy"}
        if platform == "meta_ads": return {"provider":"mock", "model":"marketmind-ads-copy"}
        return {"provider":"mock", "model":"marketmind-copy"}
