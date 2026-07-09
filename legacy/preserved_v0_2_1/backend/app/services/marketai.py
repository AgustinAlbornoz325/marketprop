import random

SEPARATORS=["━━━━━━━━━━━━","▬▬▬▬▬▬▬","────────────","✦ ✦ ✦ ✦ ✦","◆ ◆ ◆ ◆ ◆"]
STYLES=["profesional","premium","emocional","urgencia","inversor","directo","familiar","minimalista"]

def score():
    return random.randint(86,98)

def pick_style(style=None):
    return style if style and style!="auto" else random.choice(STYLES)

def base_lines(d):
    rows=[]
    if d.get("location"): rows.append(f"📍 Ubicación: {d['location']}")
    if d.get("bedrooms"): rows.append(f"🛏️ Dormitorios / ambientes: {d['bedrooms']}")
    if d.get("bathrooms"): rows.append(f"🚿 Baños: {d['bathrooms']}")
    if d.get("surface"): rows.append(f"📐 Superficie: {d['surface']}")
    if d.get("features"): rows.append("✅ Detalles: "+" · ".join(d["features"]))
    return rows

def hook(d,style):
    t=d.get("property_type","Propiedad")
    loc=d.get("location","ubicación destacada")
    price=d.get("price","Consultar precio")
    options={
        "profesional":[f"{t} en venta en {loc}",f"Oportunidad inmobiliaria en {loc}",f"{price} — {t} en venta"],
        "premium":[f"Una propiedad para destacar en {loc}",f"{t} con presencia, ubicación y potencial",f"Exclusiva oportunidad en {loc}"],
        "emocional":[f"El lugar donde puede empezar una nueva etapa",f"Una propiedad pensada para vivir mejor",f"Tu próximo espacio puede estar en {loc}"],
        "urgencia":[f"Atención: oportunidad disponible en {loc}",f"{t} en venta — consultá antes de que se reserve",f"Oportunidad activa por tiempo limitado"],
        "inversor":[f"{t} con potencial de inversión",f"Ubicación + precio + demanda: una oportunidad para mirar",f"Activo inmobiliario en {loc}"],
        "directo":[f"{t} en venta",f"{price} · {loc}",f"{t} disponible en {loc}"],
        "familiar":[f"Un espacio para disfrutar todos los días",f"{t} ideal para una nueva etapa familiar",f"Comodidad y ubicación para vivir mejor"],
        "minimalista":[f"{t} · {loc}",f"{price}",f"{t} en venta"]
    }
    return random.choice(options.get(style,options["profesional"]))

def cta(platform,style):
    ctas={
        "facebook":["📲 Consultame y te paso más información.","💬 Escribime para coordinar una visita.","📩 Pedime los detalles por privado."],
        "instagram":["📩 Escribime y te envío más info.","Guardalo y consultame por mensaje.","Mandame DM para recibir detalles."],
        "whatsapp":["Si querés, te paso más detalles.","¿Te gustaría coordinar una visita?","Te puedo enviar más información cuando quieras."],
        "mercado_libre":["Consultá para coordinar una visita.","Comunicate para recibir más información.","Solicitá más datos sin compromiso."],
        "meta_ads":["Enviar mensaje"]
    }
    return random.choice(ctas.get(platform,ctas["facebook"]))

def facebook(d,style=None):
    style=pick_style(style)
    sep=random.choice(SEPARATORS)
    lines=base_lines(d)
    random.shuffle(lines)
    return "\n".join([f"💎 {hook(d,style).upper()}",sep,*lines,sep,cta("facebook",style)])

def instagram(d,style=None):
    style=pick_style(style)
    lines=base_lines(d)
    random.shuffle(lines)
    hashtags={
        "premium":"#propiedadespremium #realestate #inmobiliaria #venta",
        "inversor":"#inversioninmobiliaria #renta #propiedades #oportunidad",
        "minimalista":"#propiedades #venta #inmobiliaria",
        "auto":"#inmobiliaria #propiedades #venta #bienesraices"
    }
    return "\n".join([f"✨ {hook(d,style)}","",random.choice(["Una propiedad con detalles para destacar.","Ubicación, funcionalidad y potencial en una sola oportunidad.","Ideal para quienes buscan tomar una buena decisión inmobiliaria."]),"",*lines,"",cta("instagram",style),hashtags.get(style,"#inmobiliaria #propiedades #venta #bienesraices")])

def whatsapp(d,style=None):
    style=pick_style(style)
    variants=[
        ["Hola! Te paso esta propiedad 👇",hook(d,style),f"📍 {d.get('location')}",f"💰 {d.get('price')}",f"🔗 {d.get('url')}",cta("whatsapp",style)],
        [f"Te comparto una opción que puede interesarte:",f"{d.get('property_type')} en {d.get('location')}",f"Precio: {d.get('price')}",f"Link: {d.get('url')}",cta("whatsapp",style)],
        [f"📌 Nueva propiedad disponible",f"Tipo: {d.get('property_type')}",f"Zona: {d.get('location')}",f"Valor: {d.get('price')}",f"Más info: {d.get('url')}"]
    ]
    return "\n".join(random.choice(variants))

def mercado(d,style=None):
    style=pick_style(style)
    desc=d.get("description") or "Propiedad en venta con excelente potencial."
    return "\n".join([hook(d,style),"",desc,"",*base_lines(d),"",f"Precio: {d.get('price')}",cta("mercado_libre",style)])

def meta(d,style=None):
    style=pick_style(style)
    return {
        "headline_1": hook(d,style)[:40],
        "headline_2": f"{d.get('price')} · Consultá hoy"[:40],
        "primary_text": random.choice([
            f"Encontrá una propiedad con excelente potencial en {d.get('location')}. Pedí más información y coordiná una visita.",
            f"Conocé esta oportunidad inmobiliaria. Información clara, atención rápida y consulta directa.",
            f"Propiedad disponible para quienes buscan ubicación, valor y proyección."
        ]),
        "cta": "Enviar mensaje",
        "style": style
    }

def generate_all_content(d,style="auto"):
    return {
        "facebook":{"score":score(),"style":pick_style(style),"text":facebook(d,style)},
        "instagram":{"score":score(),"style":pick_style(style),"text":instagram(d,style)},
        "whatsapp":{"score":score(),"style":pick_style(style),"text":whatsapp(d,style)},
        "mercado_libre":{"score":score(),"style":pick_style(style),"text":mercado(d,style)},
        "meta_ads":{"score":score(),"style":pick_style(style),"text":meta(d,style)}
    }

def generate_variation(platform,d,style="auto"):
    generators={
        "facebook":facebook,
        "instagram":instagram,
        "whatsapp":whatsapp,
        "mercado_libre":mercado,
        "meta_ads":meta
    }
    fn=generators.get(platform,facebook)
    chosen=pick_style(style)
    return {"score":score(),"style":chosen,"text":fn(d,chosen)}
