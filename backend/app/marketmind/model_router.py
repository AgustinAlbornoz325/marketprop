import os
from app.marketmind.providers.registry import provider_registry
class ModelRouter:
    def choose_model(self, task_type:str, platform:str|None=None)->dict:
        if provider_registry.demo_mode(): return {"provider":"mock","model":"marketmind-local-demo","reason":"DEMO_MODE=true"}
        if platform=="tiktok": pref=["anthropic","openai","google","mock"]
        elif platform=="meta_ads": pref=["openai","anthropic","google","mock"]
        elif platform=="whatsapp": pref=["anthropic","openai","google","mock"]
        elif platform=="mercado_libre": pref=["openai","google","anthropic","mock"]
        else: pref=[x.strip() for x in os.getenv("MARKETMIND_PROVIDER_PRIORITY","openai,anthropic,google,mock").split(",")]
        for name in pref:
            p=provider_registry.providers.get(name)
            if p and p.available(): return {"provider":name,"model":getattr(p,"model","marketmind-local-demo"),"reason":"mejor disponible para la tarea"}
        return {"provider":"mock","model":"marketmind-local-demo","reason":"sin API keys"}
    def get_provider(self, task_type:str, platform:str|None=None): return provider_registry.get(self.choose_model(task_type,platform)["provider"])
    def provider_status(self)->dict: return {"demo_mode":provider_registry.demo_mode(),"providers":provider_registry.status()}
