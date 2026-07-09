import random

def _loc(p): return p.get("location", "Ubicación a confirmar")
def _ptype(p): return p.get("type", "Propiedad")
def _price(p): return p.get("price", "Consultar precio")
def _url(p): return p.get("url", "")

ANGLES = {
    "auto": ["ubicación", "comodidad", "oportunidad", "decisión inteligente", "estilo de vida"],
    "profesional": ["información clara", "consulta directa", "evaluación tranquila", "decisión segura"],
    "premium": ["presencia", "diferencial", "estilo de vida", "calidad percibida", "proyección"],
    "urgencia": ["disponibilidad", "consulta hoy", "no dejar pasar", "oportunidad activa", "reserva"],
    "inversor": ["potencial", "demanda", "renta", "resguardo de valor", "reventa"]
}

def _angle(style):
    return random.choice(ANGLES.get(style, ANGLES["auto"]))

class FacebookAgent:
    platform = "facebook"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype, price, url = _loc(p), _ptype(p), _price(p), _url(p)
        angle = _angle(style)
        templates = {
            "auto": [
                f"""🏡 {ptype} disponible en {loc}

Si estás buscando una propiedad para mudarte, invertir o simplemente comparar opciones reales del mercado, esta puede ser una buena alternativa para mirar con atención.

📍 Zona: {loc}
💰 Valor: {price}
🔗 Link: {url}

Lo interesante de esta publicación es que no apunta solo a mostrar una propiedad, sino a ayudarte a evaluar si realmente encaja con lo que estás buscando.

📲 Escribime y te paso más información.""",
                f"""Nueva oportunidad inmobiliaria en {loc} 🏡

Hay propiedades que vale la pena mirar con calma, no solo por lo que muestran en fotos, sino por el potencial que pueden tener según ubicación, uso y momento de compra.

📍 {loc}
💰 {price}
🔗 {url}

Si querés, te paso más detalles y la analizamos juntos."""
            ],
            "profesional": [
                f"""Propiedad disponible para consulta

Tipo: {ptype}
Ubicación: {loc}
Valor: {price}

Una opción para quienes buscan información clara, consulta directa y la posibilidad de coordinar una visita sin vueltas.

Link:
{url}

📲 Consultame y te envío ficha completa.""",
                f"""{ptype} en {loc}

Publicación con información clara para que puedas evaluar la propiedad antes de avanzar.

• Zona: {loc}
• Valor: {price}
• Consulta directa
• Posibilidad de coordinar visita

🔗 {url}

Escribime para recibir más información."""
            ],
            "premium": [
                f"""✨ {ptype} con presencia en {loc}

Una propiedad para quienes buscan algo más que metros cuadrados: ubicación, sensación de hogar y una propuesta que se destaque.

📍 {loc}
💰 {price}
🔗 {url}

Si estás buscando una opción con mejor percepción, buen entorno y potencial, escribime y te paso más información.""",
                f"""Hay propiedades que se notan distintas desde el primer vistazo.

Esta opción en {loc} combina ubicación, presencia y potencial para quien está buscando comprar con criterio.

📍 Zona: {loc}
💰 {price}
🔗 {url}

📲 Pedime más información."""
            ],
            "urgencia": [
                f"""⚡ Propiedad disponible ahora en {loc}

Si estás buscando una oportunidad activa, esta es una de esas opciones que conviene consultar antes de dejarla pasar.

📍 Zona: {loc}
💰 Valor: {price}
🔗 {url}

📲 Escribime hoy y te confirmo disponibilidad.""",
                f"""Atención si estás buscando {ptype.lower()} en {loc}

Esta propiedad está disponible para consulta y puede ser una buena opción para coordinar visita cuanto antes.

💰 {price}
🔗 {url}

📲 Mandame mensaje y te paso más detalles."""
            ],
            "inversor": [
                f"""📈 {ptype} para analizar con mirada de inversión

No se trata solo de comprar una propiedad, sino de entender ubicación, demanda y potencial futuro.

📍 Zona: {loc}
💰 Valor: {price}
🔗 {url}

Puede ser interesante para renta, reventa o resguardo de valor.

📲 Escribime y la evaluamos.""",
                f"""Oportunidad inmobiliaria para mirar con números

Tipo: {ptype}
Zona: {loc}
Valor: {price}

Una propiedad que puede tener sentido para quien busca potencial, demanda y una decisión patrimonial.

🔗 {url}

📲 Consultame y te paso más información."""
            ]
        }
        return random.choice(templates.get(style, templates["auto"]))

class InstagramAgent:
    platform = "instagram"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype, price = _loc(p), _ptype(p), _price(p)
        templates = {
            "auto": [
                f"""✨ Una propiedad para mirar con calma

A veces la oportunidad no está solo en el precio.
También está en la ubicación, el momento y en cómo esa propiedad puede encajar con lo que estás buscando.

📍 {loc}
💰 {price}

Guardala para verla después o escribime y te paso más info.

#inmobiliaria #propiedades #bienesraices #venta #argentina""",
                f"""🏡 {ptype} en {loc}

Una opción para quienes están buscando algo real, claro y disponible.

📩 Pedime más información por mensaje.
💰 {price}

#propiedades #inmobiliaria #realestate #rosario #argentina"""
            ],
            "profesional": [
                f"""Información clara. Consulta directa.

{ptype} disponible en {loc}.
Una opción para evaluar con tranquilidad antes de avanzar.

💰 {price}
📩 Escribime y te paso detalles.

#inmobiliaria #propiedades #venta""",
                f"""{ptype} disponible

📍 {loc}
💰 {price}

Si estás buscando una propiedad y querés información ordenada, escribime y te envío más detalles.

#bienesraices #propiedades #inmobiliaria"""
            ],
            "premium": [
                f"""✨ Hay propiedades que transmiten distinto

Esta opción en {loc} se destaca por presencia, ubicación y potencial.

Para quienes buscan algo más que una propiedad: una decisión con estilo.

📩 Escribime y te paso más info.

#realestate #propiedadespremium #inmobiliaria""",
                f"""Una propiedad con otra presencia.

📍 {loc}
💰 {price}

Ideal para quienes valoran ubicación, estética y proyección.

Guardala o escribime para conocer más.

#propiedades #premiumrealestate #bienesraices"""
            ],
            "urgencia": [
                f"""⚡ Disponible ahora

Si estás buscando propiedad en {loc}, esta opción conviene verla antes de dejarla pasar.

📩 Mandame mensaje y te confirmo disponibilidad.

#propiedades #venta #inmobiliaria""",
                f"""No la dejes para después.

{ptype} disponible en {loc}.
💰 {price}

📩 Escribime y te paso el link completo.

#oportunidad #propiedades #inmobiliaria"""
            ],
            "inversor": [
                f"""📈 Mirala como inversión, no solo como propiedad.

Ubicación, demanda y potencial son los tres puntos que hacen interesante esta opción.

📍 {loc}
💰 {price}

📩 Escribime y la analizamos.

#inversioninmobiliaria #realestate #propiedades""",
                f"""Hay propiedades que se compran por lo que pueden llegar a valer.

{ptype} en {loc}
💰 {price}

Una opción para evaluar con mirada de inversor.

#inversion #bienesraices #propiedades"""
            ]
        }
        return random.choice(templates.get(style, templates["auto"]))

class TikTokAgent:
    platform = "tiktok"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype = _loc(p), _ptype(p)
        hooks = {
            "auto": [
                "Antes de comprar una propiedad, mirá este detalle",
                "No empieces mirando los metros: empezá por esto",
                "Si estás buscando propiedad, esto te puede ahorrar tiempo"
            ],
            "profesional": [
                "Tres cosas que revisaría antes de visitar esta propiedad",
                "Cómo analizar una propiedad sin perder tiempo",
                "Antes de consultar, mirá estos puntos"
            ],
            "premium": [
                "No todas las propiedades se sienten iguales al entrar",
                "Esta propiedad tiene algo que no se explica solo con metros",
                "Mirá por qué esta propiedad se percibe diferente"
            ],
            "urgencia": [
                "Si estás buscando propiedad, no dejes esta para después",
                "Esta es de las opciones que conviene consultar rápido",
                "Si te interesa, preguntá antes de que se reserve"
            ],
            "inversor": [
                "No compres una propiedad sin mirar este factor",
                "Esto separa una compra común de una buena inversión",
                "Mirá esta propiedad con ojos de inversor"
            ]
        }
        structures = [
            f"""🎬 Hook hablado:
“{random.choice(hooks.get(style, hooks["auto"]))}”

Guion:
1. Mostrá la fachada o el mejor ambiente.
2. Decí: “Esta propiedad está en {loc} y puede servir para quienes buscan {ptype.lower()} con potencial.”
3. Mostrá 2 detalles concretos.
4. Cerrá con: “Comentá INFO y te paso el link.”

Texto en pantalla:
“¿La verías?”

CTA:
Comentá “INFO”.""",
            f"""🎬 Idea de Reel/TikTok:
Arrancá con una toma rápida y una frase fuerte.

Hook:
“{random.choice(hooks.get(style, hooks["auto"]))}”

Estructura:
0-2s: mejor toma de la propiedad.
3-6s: explicar el punto fuerte.
7-10s: mostrar ubicación o beneficio.
11-13s: CTA.

CTA hablado:
“Mandame mensaje y te paso más detalles.”""",
            f"""🎬 Video corto para {ptype} en {loc}

Primer segundo:
“{random.choice(hooks.get(style, hooks["auto"]))}”

Después:
- Mostrá recorrido rápido.
- Marcá un detalle que la diferencie.
- Cerrá con una pregunta.

Texto final:
“¿Querés verla completa?”

CTA:
Mandá “INFO”."""
        ]
        return random.choice(structures)

class WhatsAppAgent:
    platform = "whatsapp"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype, price, url = _loc(p), _ptype(p), _price(p), _url(p)
        templates = {
            "auto": [
                f"""Hola! Te paso esta propiedad que puede interesarte 👇

{ptype} en {loc}
💰 {price}
🔗 {url}

Si querés, te paso más detalles o coordinamos para verla.""",
                f"""Hola! Mirá esta opción que encontré:

📍 {loc}
🏡 {ptype}
💰 {price}

Te dejo el link:
{url}

¿Querés que te mande más info?"""
            ],
            "profesional": [
                f"""Hola! Te comparto la información de esta propiedad:

Tipo: {ptype}
Zona: {loc}
Valor: {price}
Link: {url}

Si te interesa, puedo pasarte más detalles o coordinar una visita.""",
                f"""Hola, ¿cómo estás? Te paso una opción para evaluar:

{ptype} en {loc}
Valor: {price}

{url}

Decime si querés que te envíe la ficha completa."""
            ],
            "premium": [
                f"""Hola! Te paso una propiedad con muy buena presencia en {loc}.

🏡 {ptype}
💰 {price}
🔗 {url}

Creo que puede interesarte si buscás algo con mejor ubicación y más diferencial.

¿Querés que te pase más detalles?""",
                f"""Hola! Esta opción me pareció interesante para que la veas tranquilo.

📍 {loc}
🏡 {ptype}
💰 {price}

{url}

Tiene un perfil más premium. Si te gusta, la vemos en detalle."""
            ],
            "urgencia": [
                f"""Hola! Te paso esta opción porque está disponible ahora:

{ptype} en {loc}
💰 {price}
🔗 {url}

Si te interesa, conviene consultarla hoy. ¿Querés que averigüe disponibilidad?""",
                f"""Hola! Esta propiedad está activa y puede moverse rápido.

📍 {loc}
🏡 {ptype}
💰 {price}

{url}

¿Querés que pregunte si sigue disponible?"""
            ],
            "inversor": [
                f"""Hola! Te comparto esta opción para analizar como inversión.

{ptype} en {loc}
💰 {price}
🔗 {url}

Puede ser interesante por ubicación/potencial. Si querés, la vemos con números.""",
                f"""Hola! Mirá esta propiedad con mirada de inversión:

📍 {loc}
🏡 {ptype}
💰 {price}

{url}

Si te interesa, te paso más datos para evaluar rentabilidad/potencial."""
            ]
        }
        return random.choice(templates.get(style, templates["auto"]))

class MercadoLibreAgent:
    platform = "mercado_libre"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype, price = _loc(p), _ptype(p), _price(p)
        openings = {
            "auto": "Propiedad disponible para consulta.",
            "profesional": "Publicación clara y ordenada para evaluar esta propiedad.",
            "premium": "Propiedad destacada por ubicación, presentación y potencial.",
            "urgencia": "Propiedad disponible actualmente para consulta inmediata.",
            "inversor": "Oportunidad inmobiliaria para analizar con mirada de inversión."
        }
        sections = [
            f"""{openings.get(style, openings["auto"])}

Características principales:
- Tipo de propiedad: {ptype}
- Ubicación: {loc}
- Valor: {price}
- Operación: consultar
- Disponibilidad: a confirmar

Descripción:
Opción ideal para quienes buscan una propiedad clara, funcional y con posibilidad de coordinar visita.

Consultas:
Escribinos para recibir más información, fotos, medidas o coordinar una visita.""",
            f"""{ptype} en {loc}

Descripción:
Propiedad disponible para quienes buscan una alternativa concreta dentro del mercado actual.

Datos destacados:
- Zona: {loc}
- Tipo: {ptype}
- Precio: {price}
- Consulta directa

Para más información, solicitá detalles y coordinamos una visita."""
        ]
        return random.choice(sections)

class MetaAdsAgent:
    platform = "meta_ads"
    def run(self, p, s):
        style = s.get("style", "auto")
        loc, ptype = _loc(p), _ptype(p)
        sets = {
            "auto": [
                {"titulo_1": f"{ptype} en {loc}", "titulo_2": "Pedí información", "texto_principal": f"Conocé esta propiedad en {loc}. Recibí detalles y coordiná una visita.", "descripcion": "Consulta directa", "cta": "Enviar mensaje"},
                {"titulo_1": "Nueva oportunidad", "titulo_2": f"Disponible en {loc}", "texto_principal": "Una propiedad para evaluar con tranquilidad. Solicitá más información por mensaje.", "descripcion": "Propiedad disponible", "cta": "Más información"}
            ],
            "profesional": [
                {"titulo_1": "Consultá esta propiedad", "titulo_2": "Información clara", "texto_principal": f"{ptype} disponible en {loc}. Pedí ficha completa y coordiná una visita.", "descripcion": "Atención directa", "cta": "Enviar mensaje"}
            ],
            "premium": [
                {"titulo_1": "Propiedad destacada", "titulo_2": f"{loc}", "texto_principal": "Una opción con presencia, ubicación y potencial. Escribinos para conocer más.", "descripcion": "Consulta premium", "cta": "Enviar mensaje"}
            ],
            "urgencia": [
                {"titulo_1": "Disponible ahora", "titulo_2": "Consultá hoy", "texto_principal": f"{ptype} en {loc}. Si te interesa, pedí información antes de que se reserve.", "descripcion": "Oportunidad activa", "cta": "Enviar mensaje"}
            ],
            "inversor": [
                {"titulo_1": "Invertí en propiedad", "titulo_2": f"Potencial en {loc}", "texto_principal": "Analizá esta oportunidad inmobiliaria con foco en ubicación, demanda y proyección.", "descripcion": "Para inversores", "cta": "Más información"}
            ]
        }
        result = random.choice(sets.get(style, sets["auto"]))
        result["angulo"] = s.get("primary_angle", style)
        return result
