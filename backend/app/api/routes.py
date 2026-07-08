from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random, re

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    organization_name: str
    email: str
    password: str

class GenerateRequest(BaseModel):
    url: str
    style: str = "auto"

class VariationRequest(BaseModel):
    platform: str
    property_data: dict
    style: str = "auto"

STYLES = ["auto", "profesional", "premium", "urgencia", "inversor"]

def ok(style):
    return style if style in STYLES else "auto"

def user(name="Agustín", org="Forja Propiedades"):
    return {"name": name, "organization_name": org, "plan": "Plan Básico"}

@router.post("/auth/login")
def login(req: LoginRequest):
    if not req.email or not req.password:
        raise HTTPException(400, "Completá email y contraseña.")
    return {"token": "demo-token", "user": user()}

@router.post("/auth/register")
def register(req: RegisterRequest):
    if not req.name or not req.organization_name or not req.email or not req.password:
        raise HTTPException(400, "Completá todos los campos.")
    return {"token": "demo-token", "user": user(req.name, req.organization_name)}

def infer_property(url):
    u = url.lower()
    ptype = "Propiedad"
    if "casa" in u: ptype = "Casa"
    elif "departamento" in u or "depto" in u: ptype = "Departamento"
    elif "terreno" in u or "lote" in u: ptype = "Terreno"
    elif "local" in u: ptype = "Local"

    loc = "Ubicación a confirmar"
    places = {"rosario":"Rosario", "funes":"Funes", "pichincha":"Pichincha", "fisherton":"Fisherton", "centro":"Centro", "palermo":"Palermo", "eche":"Echesortu"}
    for k,v in places.items():
        if k in u:
            loc = v
            break

    return {"url": url, "type": ptype, "location": loc, "price": "Consultar precio"}

HOOKS = {
    "facebook": {
        "auto": ["Nueva oportunidad inmobiliaria para mirar con atención", "Si estás buscando propiedad, esta opción puede interesarte", "Una propiedad que puede encajar con tu búsqueda"],
        "profesional": ["Propiedad disponible con información clara y consulta directa", "Opción inmobiliaria para evaluar con tranquilidad", "Conocé esta propiedad y analizá su potencial"],
        "premium": ["Una propiedad con presencia, ubicación y potencial", "Para quienes buscan algo más que metros cuadrados", "Una opción con detalles que la hacen destacar"],
        "urgencia": ["Esta oportunidad puede no durar mucho", "Propiedad disponible para consultar hoy", "Si te interesa, conviene verla cuanto antes"],
        "inversor": ["Una propiedad para mirar con ojos de inversor", "Ubicación, demanda y potencial en una misma oportunidad", "No mires solo el precio: mirá el potencial"]
    },
    "instagram": {
        "auto": ["Una propiedad que merece guardarse", "Tu próxima oportunidad puede estar acá", "Una opción ideal para mirar con calma"],
        "profesional": ["Una opción clara para quienes buscan decidir bien", "Ubicación, potencial y consulta directa", "Una propiedad para evaluar con tranquilidad"],
        "premium": ["Una propiedad con estética, ubicación y proyección", "El tipo de propiedad que se destaca sin decir demasiado", "Para quienes buscan una oportunidad con presencia"],
        "urgencia": ["Guardala antes de que deje de estar disponible", "Si te gustó, no la dejes para después", "Una oportunidad activa para consultar hoy"],
        "inversor": ["Una propiedad para mirar con ojos de inversor", "Hay propiedades que se compran por lo que pueden llegar a valer", "Potencial, ubicación y demanda en una sola oportunidad"]
    },
    "tiktok": {
        "auto": ["No empieces mirando la casa: mirá este detalle primero", "Esto es lo primero que revisaría antes de comprar", "Si estás buscando propiedad, prestá atención a esto"],
        "profesional": ["Antes de visitar una propiedad, mirá este punto", "Este detalle puede cambiar tu decisión", "No analices una propiedad sin mirar esto"],
        "premium": ["No todas las propiedades transmiten esto en el primer vistazo", "Mirá por qué esta propiedad se siente diferente", "Hay propiedades que se venden por cómo te hacen imaginar vivir ahí"],
        "urgencia": ["Si estás buscando propiedad, mirá esto antes de que se reserve", "Esta oportunidad puede durar menos de lo que pensás", "No la guardes para después si realmente estás buscando"],
        "inversor": ["No compres una propiedad sin mirar este factor", "Esto separa una compra común de una buena inversión", "Mirá esta propiedad como inversor, no como comprador común"]
    },
    "whatsapp": {
        "auto": ["Te comparto una propiedad que puede interesarte", "Mirá esta opción que encontré", "Te paso una propiedad para que la veas tranquilo"],
        "profesional": ["Te comparto una opción para evaluar con tranquilidad", "Te paso la información de esta propiedad", "Esta opción puede servirte si estás buscando algo claro"],
        "premium": ["Te comparto una opción con muy buena presencia", "Esta propiedad tiene detalles interesantes para analizar", "Creo que esta opción puede encajar con lo que buscás"],
        "urgencia": ["Te paso esta opción porque está disponible ahora", "Esta propiedad conviene verla cuanto antes", "Si te interesa, podemos consultarla hoy"],
        "inversor": ["Te comparto una opción interesante para evaluar como inversión", "Esta propiedad puede tener buen potencial", "Te paso una oportunidad para mirar con números"]
    },
    "mercado_libre": {
        "auto": ["Propiedad en venta", "Oportunidad inmobiliaria disponible", "Propiedad disponible para consulta"],
        "profesional": ["Propiedad publicada con información clara", "Opción inmobiliaria para evaluar", "Propiedad disponible para coordinar visita"],
        "premium": ["Propiedad destacada", "Propiedad con atributos diferenciales", "Oportunidad con excelente presentación"],
        "urgencia": ["Propiedad disponible para consulta inmediata", "Oportunidad activa", "Propiedad con disponibilidad actual"],
        "inversor": ["Propiedad con potencial de inversión", "Oportunidad inmobiliaria para analizar rentabilidad", "Activo inmobiliario disponible"]
    },
    "meta_ads": {
        "auto": ["Conocé esta propiedad", "Pedí información por esta oportunidad", "Propiedad disponible para consulta"],
        "profesional": ["Consultá por esta propiedad", "Coordiná una visita", "Recibí información completa"],
        "premium": ["Propiedad destacada", "Una oportunidad con presencia", "Conocé una propiedad diferente"],
        "urgencia": ["Consultá antes de que se reserve", "Oportunidad disponible hoy", "Pedí información ahora"],
        "inversor": ["Analizá esta oportunidad", "Propiedad con potencial", "Invertí en ubicación y demanda"]
    }
}

def pick(platform, style):
    return random.choice(HOOKS[platform][ok(style)])

def facebook_agent(p, style):
    h = pick("facebook", style)
    return f"""🏡 {h.upper()}

Una propiedad para quienes están buscando tomar una buena decisión inmobiliaria.

📍 Zona: {p['location']}
💰 Valor: {p['price']}
🔗 Link: {p['url']}

¿Por qué puede interesarte?
• Buena oportunidad para analizar
• Consulta directa
• Ideal para comparar con otras opciones del mercado

📲 Escribime y te paso más información."""

def instagram_agent(p, style):
    h = pick("instagram", style)
    return f"""✨ {h}

Una propiedad no se elige solo por los metros.
También importa la ubicación, el potencial y cómo encaja con tu momento.

📍 {p['location']}
💰 {p['price']}

Guardala para verla después o escribime y te paso más detalles.

#inmobiliaria #propiedades #bienesraices #venta #argentina"""

def tiktok_agent(p, style):
    h = pick("tiktok", style)
    return f"""🎬 Hook hablado:
“{h}”

Guion corto:
1. Primer segundo: mostrar el problema o la curiosidad.
2. Segundo 2-5: mostrar el mejor ángulo de la propiedad.
3. Segundo 6-12: explicar por qué conviene verla.
4. Cierre: “Escribime y te paso el link completo.”

Texto en pantalla:
“Antes de comprar, mirá esto.”

CTA:
Comentá “INFO” o mandame mensaje."""

def whatsapp_agent(p, style):
    h = pick("whatsapp", style)
    return f"""Hola! {h} 👇

📍 Zona: {p['location']}
💰 Valor: {p['price']}
🔗 {p['url']}

Si querés, te paso más detalles o coordinamos para verla."""

def mercadolibre_agent(p, style):
    h = pick("mercado_libre", style)
    return f"""{h}

Descripción:
Propiedad disponible para consulta, ideal para quienes buscan una opción clara, funcional y con potencial.

Características principales:
- Tipo: {p['type']}
- Ubicación: {p['location']}
- Precio: {p['price']}
- Consulta directa

Coordiná una visita o solicitá más información."""

def meta_ads_agent(p, style):
    h = pick("meta_ads", style)
    return {"titulo_1": h[:40], "titulo_2": "Consultá por WhatsApp", "texto_principal": f"{h}. Recibí información completa y coordiná una visita.", "descripcion": "Propiedad disponible", "cta": "Enviar mensaje"}

AGENTS = {
    "facebook": facebook_agent,
    "instagram": instagram_agent,
    "tiktok": tiktok_agent,
    "whatsapp": whatsapp_agent,
    "mercado_libre": mercadolibre_agent,
    "meta_ads": meta_ads_agent
}

def score(platform, style):
    bonus = 2 if platform in ["instagram", "tiktok", "meta_ads"] else 0
    bonus += 1 if style in ["premium", "inversor"] else 0
    return min(random.randint(86, 96) + bonus, 99)

@router.post("/generate")
def generate(req: GenerateRequest):
    if not req.url.startswith(("http://", "https://")):
        raise HTTPException(400, "Pegá un link válido que empiece con http:// o https://")
    p = infer_property(req.url)
    s = ok(req.style)
    content = {}
    for platform, agent in AGENTS.items():
        content[platform] = {"score": score(platform, s), "style": s, "agent": agent.__name__.replace("_agent", ""), "text": agent(p, s)}
    return {"property": p, "content": content}

@router.post("/variation")
def variation(req: VariationRequest):
    if req.platform not in AGENTS:
        raise HTTPException(400, "Plataforma no soportada.")
    p = req.property_data or infer_property("")
    s = ok(req.style)
    agent = AGENTS[req.platform]
    return {"platform": req.platform, "variation": {"score": score(req.platform, s), "style": s, "agent": agent.__name__.replace("_agent", ""), "text": agent(p, s)}}
