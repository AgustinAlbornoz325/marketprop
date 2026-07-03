import random
SEP=["━━━━━━━━━━━━","▬▬▬▬▬▬▬","────────────","✦ ✦ ✦ ✦ ✦"]
EM=["💎","🏡","✨","🔥","📍","🚀"]
def score(): return random.randint(84,97)
def lines(d):
    out=[]
    if d.get("location"): out.append(f"📍 Ubicación: {d['location']}")
    if d.get("bedrooms"): out.append(f"🛏️ Dormitorios / ambientes: {d['bedrooms']}")
    if d.get("bathrooms"): out.append(f"🚿 Baños: {d['bathrooms']}")
    if d.get("surface"): out.append(f"📐 Superficie: {d['surface']}")
    if d.get("features"): out.append("✅ Detalles: "+" · ".join(d["features"]))
    return out
def facebook(d): return "\n".join([f"{random.choice(EM)} {d.get('price')} — {d.get('property_type','Propiedad').upper()} EN VENTA",random.choice(SEP),*lines(d),random.choice(SEP),"📲 Consultame y te paso más información."])
def instagram(d): return "\n".join([f"✨ {d.get('property_type','Propiedad')} en venta",f"📍 {d.get('location')}","","Una oportunidad ideal para quienes buscan ubicación, comodidad y buena proyección.","",*lines(d),"","📩 Escribime para recibir más info.","#inmobiliaria #propiedades #rosario #venta"])
def whatsapp(d): return "\n".join(["Hola! Te paso esta propiedad 👇",f"{d.get('property_type')} en venta",f"📍 {d.get('location')}",f"💰 {d.get('price')}",f"🔗 {d.get('url')}","Si querés, te paso más detalles."])
def mercado(d): return "\n".join([f"{d.get('property_type')} en venta - {d.get('location')}","",d.get("description") or "Propiedad en venta con excelente potencial.","",*lines(d),"",f"Precio: {d.get('price')}","Consultá para coordinar una visita."])
def meta(d): return {"headline_1":f"{d.get('property_type')} en {d.get('location')}","headline_2":f"{d.get('price')} · Consultá hoy","primary_text":"Encontrá una propiedad con excelente potencial. Pedí más información y coordiná una visita.","cta":"Enviar mensaje"}
def generate_all_content(d): return {"facebook":{"score":score(),"text":facebook(d)},"instagram":{"score":score(),"text":instagram(d)},"whatsapp":{"score":score(),"text":whatsapp(d)},"mercado_libre":{"score":score(),"text":mercado(d)},"meta_ads":{"score":score(),"text":meta(d)}}
def generate_variation(platform,d): return generate_all_content(d).get(platform,{"score":score(),"text":facebook(d)})
