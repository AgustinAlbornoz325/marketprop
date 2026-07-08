from app.marketmind.model_router import ModelRouter
from app.marketmind.evaluator import Evaluator
from app.marketmind.memory import memory_store
from app.marketmind.agents.property_agent import PropertyAgent
from app.marketmind.agents.copy_agent import CopyAgent
from app.marketmind.agents.editor_agent import EditorAgent
from app.marketmind.agents.platform_agents import FacebookAgent, InstagramAgent, TikTokAgent, WhatsAppAgent, MercadoLibreAgent, MetaAdsAgent
PLATFORM_AGENTS = {"facebook":FacebookAgent(), "instagram":InstagramAgent(), "tiktok":TikTokAgent(), "whatsapp":WhatsAppAgent(), "mercado_libre":MercadoLibreAgent(), "meta_ads":MetaAdsAgent()}
class MarketMindOrchestrator:
    def __init__(self):
        self.router = ModelRouter(); self.evaluator = Evaluator(); self.property_agent = PropertyAgent(); self.copy_agent = CopyAgent(); self.editor = EditorAgent()
    def generate(self, url: str, style: str = "auto") -> dict:
        trace = [{"step":"input", "message":"Usuario pegó link de propiedad"}]
        p = self.property_agent.run(url); trace.append({"step":"property_agent", "message":"Agente Propiedad interpretó datos base", "data":p})
        strategy = self.copy_agent.run(p, style); trace.append({"step":"copy_agent", "message":"Agente Copy definió estrategia", "data":strategy})
        content = {}
        for platform, agent in PLATFORM_AGENTS.items():
            model = self.router.choose_model("generation", platform); trace.append({"step":"model_router", "platform":platform, "model":model})
            edited = self.editor.run(agent.run(p, strategy))
            ev = self.evaluator.evaluate(platform, edited, strategy["style"])
            attempts = 1
            if ev["decision"] == "regenerate":
                attempts = 2; edited = self.editor.run(agent.run(p, strategy)); ev = self.evaluator.evaluate(platform, edited, strategy["style"])
            content[platform] = {"agent":agent.__class__.__name__, "provider":model.get("provider"), "provider":model.get("provider"), "model":model["model"], "style":strategy["style"], "score":ev["total"], "evaluation":ev, "attempts":attempts, "text":edited}
        memory_store.remember({"event":"generation", "url":url, "style":style, "platforms":list(content.keys())})
        trace.append({"step":"delivery", "message":"MarketMind entregó contenido evaluado por plataforma"})
        return {"property":p, "strategy":strategy, "content":content, "trace":trace}
    def variation(self, platform: str, property_data: dict, style: str = "auto") -> dict:
        if platform not in PLATFORM_AGENTS: raise ValueError("Plataforma no soportada")
        strategy = self.copy_agent.run(property_data, style); agent = PLATFORM_AGENTS[platform]; model = self.router.choose_model("variation", platform)
        edited = self.editor.run(agent.run(property_data, strategy)); ev = self.evaluator.evaluate(platform, edited, strategy["style"])
        return {"platform":platform, "variation":{"agent":agent.__class__.__name__, "provider":model.get("provider"), "provider":model.get("provider"), "model":model["model"], "style":strategy["style"], "score":ev["total"], "evaluation":ev, "text":edited}}
