import random
HOOKS = {
 "facebook":["Nueva oportunidad inmobiliaria para mirar con atención", "Una propiedad que puede encajar con tu búsqueda", "Si estás buscando propiedad, esta opción puede interesarte"],
 "instagram":["Una propiedad que merece guardarse", "Tu próxima oportunidad puede estar acá", "Una opción ideal para mirar con calma"],
 "tiktok":["No empieces mirando la casa: mirá este detalle primero", "Esto es lo primero que revisaría antes de comprar", "Si estás buscando propiedad, prestá atención a esto"],
 "whatsapp":["Te comparto una propiedad que puede interesarte", "Mirá esta opción que encontré", "Te paso una propiedad para que la veas tranquilo"],
 "mercado_libre":["Propiedad en venta", "Oportunidad inmobiliaria disponible", "Propiedad disponible para consulta"],
 "meta_ads":["Conocé esta propiedad", "Pedí información por esta oportunidad", "Propiedad disponible para consulta"],
}
STYLE_MOD = {"premium":" con un enfoque premium y diferencial", "urgencia":" con foco en disponibilidad y consulta rápida", "inversor":" con mirada de inversión y potencial", "profesional":" con tono profesional y claro", "auto":""}
def _hook(platform, style): return random.choice(HOOKS[platform]) + STYLE_MOD.get(style, "")

class FacebookAgent:
    platform = "facebook"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return f"""🏡 {h.upper()}\n\nUna propiedad para quienes están buscando tomar una buena decisión inmobiliaria.\n\n📍 Zona: {p['location']}\n💰 Valor: {p['price']}\n🔗 Link: {p['url']}\n\n¿Por qué puede interesarte?\n• Buena oportunidad para analizar\n• Consulta directa\n• Ideal para comparar con otras opciones del mercado\n\n📲 Escribime y te paso más información."""
class InstagramAgent:
    platform = "instagram"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return f"""✨ {h}\n\nUna propiedad no se elige solo por los metros. También importa la ubicación, el potencial y cómo encaja con tu momento.\n\n📍 {p['location']}\n💰 {p['price']}\n\nGuardala para verla después o escribime y te paso más detalles.\n\n#inmobiliaria #propiedades #bienesraices #venta #argentina"""
class TikTokAgent:
    platform = "tiktok"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return f"""🎬 Hook hablado:\n“{h}”\n\nGuion corto:\n1. Primer segundo: mostrar el problema o la curiosidad.\n2. Segundo 2-5: mostrar el mejor ángulo de la propiedad.\n3. Segundo 6-12: explicar por qué conviene verla.\n4. Cierre: “Escribime y te paso el link completo.”\n\nTexto en pantalla:\n“Antes de comprar, mirá esto.”\n\nCTA:\nComentá “INFO” o mandame mensaje."""
class WhatsAppAgent:
    platform = "whatsapp"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return f"""Hola! {h} 👇\n\n📍 Zona: {p['location']}\n💰 Valor: {p['price']}\n🔗 {p['url']}\n\nSi querés, te paso más detalles o coordinamos para verla."""
class MercadoLibreAgent:
    platform = "mercado_libre"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return f"""{h}\n\nDescripción:\nPropiedad disponible para consulta, ideal para quienes buscan una opción clara, funcional y con potencial.\n\nCaracterísticas principales:\n- Tipo: {p['type']}\n- Ubicación: {p['location']}\n- Precio: {p['price']}\n- Consulta directa\n\nCoordiná una visita o solicitá más información."""
class MetaAdsAgent:
    platform = "meta_ads"
    def run(self, p, s):
        h = _hook(self.platform, s["style"])
        return {"titulo_1": h[:40], "titulo_2": "Consultá por WhatsApp", "texto_principal": f"{h}. Recibí información completa y coordiná una visita.", "descripcion": "Propiedad disponible", "cta": "Enviar mensaje", "angulo": s["primary_angle"]}
