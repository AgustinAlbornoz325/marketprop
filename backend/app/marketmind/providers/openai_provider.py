import os, httpx
class OpenAIProvider:
    name = "openai"
    def __init__(self):
        self.api_key=os.getenv("OPENAI_API_KEY",""); self.model=os.getenv("OPENAI_MODEL","gpt-5.2")
    def available(self)->bool: return bool(self.api_key)
    def complete(self, task:dict)->dict:
        if not self.available(): raise RuntimeError("OPENAI_API_KEY no configurada")
        payload={"model":task.get("model",self.model),"input":[{"role":"system","content":task.get("system","")},{"role":"user","content":task.get("prompt","")}],"max_output_tokens":task.get("max_tokens",900)}
        r=httpx.post("https://api.openai.com/v1/responses",headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},json=payload,timeout=60)
        r.raise_for_status(); data=r.json(); text=data.get("output_text")
        if not text:
            parts=[]
            for item in data.get("output",[]):
                for c in item.get("content",[]):
                    if c.get("type") in ["output_text","text"]: parts.append(c.get("text", ""))
            text="\n".join(parts).strip()
        return {"provider":self.name,"model":task.get("model",self.model),"mode":"real","text":text or task.get("fallback_text","")}
