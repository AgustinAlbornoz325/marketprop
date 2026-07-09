import os, httpx
class GoogleProvider:
    name = "google"
    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY",""); self.model=os.getenv("GEMINI_MODEL","gemini-3.5-flash")
    def available(self)->bool: return bool(self.api_key)
    def complete(self, task:dict)->dict:
        if not self.available(): raise RuntimeError("GEMINI_API_KEY no configurada")
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{task.get('model',self.model)}:generateContent?key={self.api_key}"
        payload={"systemInstruction":{"parts":[{"text":task.get("system","")}]},"contents":[{"role":"user","parts":[{"text":task.get("prompt","")}]}],"generationConfig":{"maxOutputTokens":task.get("max_tokens",900)}}
        r=httpx.post(url,json=payload,timeout=60); r.raise_for_status(); data=r.json(); parts=[]
        for cand in data.get("candidates",[]):
            for part in cand.get("content",{}).get("parts",[]):
                if "text" in part: parts.append(part["text"])
        return {"provider":self.name,"model":task.get("model",self.model),"mode":"real","text":"\n".join(parts).strip() or task.get("fallback_text","")}
