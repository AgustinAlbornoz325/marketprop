from app.marketmind.model_router import ModelRouter
from app.marketmind.evaluator import Evaluator
from app.marketmind.memory import memory_store
from app.marketmind.agents.property_agent import PropertyAgent
from app.marketmind.agents.copy_agent import CopyAgent
from app.marketmind.agents.editor_agent import EditorAgent
from app.marketmind.agents.platform_agents import FacebookAgent, InstagramAgent, TikTokAgent, WhatsAppAgent, MercadoLibreAgent, MetaAdsAgent
PLATFORM_AGENTS={"facebook":FacebookAgent(),"instagram":InstagramAgent(),"tiktok":TikTokAgent(),"whatsapp":WhatsAppAgent(),"mercado_libre":MercadoLibreAgent(),"meta_ads":MetaAdsAgent()}
class MarketMindOrchestrator:
    def __init__(self): self.router=ModelRouter(); self.evaluator=Evaluator(); self.property_agent=PropertyAgent(); self.copy_agent=CopyAgent(); self.editor=EditorAgent()
    def _system(self,platform): return f"Sos un agente experto de MarketProp. Escribí en español argentino, claro, vendedor, sin exagerar. Generá contenido específico para {platform}. Entregá solo el contenido final."
    def _prompt(self,platform,p,strategy,base): return f"PLATAFORMA: {platform}\nTIPO: {p.get('type')}\nUBICACIÓN: {p.get('location')}\nPRECIO: {p.get('price')}\nLINK: {p.get('url')}\nESTILO: {strategy.get('style')}\nÁNGULO: {strategy.get('primary_angle')}\n\nBORRADOR BASE:\n{base}\n\nMejorá este contenido para que sea más natural, específico y menos repetitivo."
    def _run_platform(self,platform,agent,p,strategy,task_type="generation"):
        model=self.router.choose_model(task_type,platform); provider=self.router.get_provider(task_type,platform); base=agent.run(p,strategy)
        try:
            res=provider.complete({"model":model["model"],"system":self._system(platform),"prompt":self._prompt(platform,p,strategy,base),"fallback_text":base,"max_tokens":900})
            text=res.get("text") or base; mode=res.get("mode","demo")
        except Exception as e:
            text=base; mode="fallback"; model={**model,"provider_error":str(e)[:180]}
        edited=self.editor.run(text); ev=self.evaluator.evaluate(platform,edited,strategy["style"])
        return {"agent":agent.__class__.__name__,"provider":model.get("provider"),"model":model.get("model"),"mode":mode,"score":ev["total"],"style":strategy["style"],"evaluation":ev,"text":edited}
    def generate(self,url,style="auto"):
        p=self.property_agent.run(url); strategy=self.copy_agent.run(p,style); content={}
        for platform,agent in PLATFORM_AGENTS.items(): content[platform]=self._run_platform(platform,agent,p,strategy,"generation")
        memory_store.remember({"event":"generation","url":url,"style":style,"providers":[v["provider"] for v in content.values()]})
        return {"property":p,"strategy":strategy,"content":content,"trace":[{"step":"real_ai_connector","message":"MarketMind eligió proveedor real o mock por plataforma"}]}
    def variation(self,platform,property_data,style="auto"):
        if platform not in PLATFORM_AGENTS: raise ValueError("Plataforma no soportada")
        strategy=self.copy_agent.run(property_data,style); return {"platform":platform,"variation":self._run_platform(platform,PLATFORM_AGENTS[platform],property_data,strategy,"variation")}
