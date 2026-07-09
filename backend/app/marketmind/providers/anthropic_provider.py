import os, httpx
class AnthropicProvider:
    name = "anthropic"
    def __init__(self):
        self.api_key=os.getenv("ANTHROPIC_API_KEY",""); self.model=os.getenv("ANTHROPIC_MODEL","claude-sonnet-4-5")
    def available(self)->bool: return bool(self.api_key)
    def complete(self, task:dict)->dict:
        if not self.available(): raise RuntimeError("ANTHROPIC_API_KEY no configurada")
        payload={"model":task.get("model",self.model),"max_tokens":task.get("max_tokens",900),"system":task.get("system",""),"messages":[{"role":"user","content":task.get("prompt","")}]} 
        r=httpx.post("https://api.anthropic.com/v1/messages",headers={"x-api-key":self.api_key,"anthropic-version":"2023-06-01","Content-Type":"application/json"},json=payload,timeout=60)
        r.raise_for_status(); data=r.json(); text="\n".join([c.get("text","") for c in data.get("content",[]) if c.get("type")=="text"])
        return {"provider":self.name,"model":task.get("model",self.model),"mode":"real","text":text or task.get("fallback_text","")}
