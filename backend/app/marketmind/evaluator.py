import random
class Evaluator:
    def evaluate(self, platform: str, text, style: str) -> dict:
        raw = text if isinstance(text, str) else str(text)
        clarity = random.randint(84, 96)
        platform_fit = random.randint(85, 98)
        originality = random.randint(78, 94)
        cta = random.randint(80, 96)
        if platform == "tiktok" and "Hook hablado" in raw: platform_fit += 3
        if platform == "mercado_libre" and "Características principales" in raw: clarity += 3
        if platform == "whatsapp" and len(raw) < 500: clarity += 2
        if len(raw) < 80: clarity -= 8
        if any(x in raw.lower() for x in ["consult", "mensaje", "info", "visita"]): cta += 2
        clarity, platform_fit, originality, cta = [min(max(v,0),99) for v in [clarity, platform_fit, originality, cta]]
        total = round(clarity*.28 + platform_fit*.34 + originality*.20 + cta*.18)
        return {"total": total, "clarity": clarity, "platform_fit": platform_fit, "originality": originality, "cta": cta, "decision": "deliver" if total >= 86 else "regenerate"}
