import re,requests
from bs4 import BeautifulSoup

def clean(t):
    return re.sub(r"\s+"," ",t or "").strip()

def meta(soup,name):
    tag=soup.find("meta",attrs={"name":name}) or soup.find("meta",attrs={"property":name})
    return clean(tag.get("content")) if tag and tag.get("content") else ""

def find_price(text):
    for pattern,prefix in [(r"USD\s?[\$]?\s?([\d\.\,]+)","USD"),(r"U\$S\s?([\d\.\,]+)","USD"),(r"\$\s?([\d\.\,]+)","$")]:
        m=re.search(pattern,text,re.I)
        if m:
            return f"{prefix} {m.group(1)}"
    return "Consultar precio"

def find_type(text):
    x=text.lower()
    if "terreno" in x or "lote" in x: return "Terreno"
    if "casa" in x: return "Casa"
    if "departamento" in x or "depto" in x: return "Departamento"
    if "local" in x: return "Local"
    if "oficina" in x: return "Oficina"
    return "Propiedad"

def find_location(text):
    places=["Rosario","Funes","Echesortu","Fisherton","Centro","Pichincha","Alberdi","Puerto Norte","Vida Jardín","Santa Fe","Palermo","Recoleta","Belgrano","Córdoba"]
    found=[p for p in places if re.search(p,text,re.I)]
    return " · ".join(dict.fromkeys(found[:2])) if found else "Ubicación a confirmar"

def find_number(text,patterns):
    for p in patterns:
        m=re.search(p,text,re.I)
        if m: return m.group(1)
    return ""

def find_surface(text):
    for p in [r"(\d+[\,\.]?\d*)\s*m2",r"(\d+[\,\.]?\d*)\s*m²",r"(\d+[\,\.]?\d*)\s*metros"]:
        m=re.search(p,text,re.I)
        if m: return f"{m.group(1)} m²"
    return ""

def find_features(text):
    kws=["cochera","balcón","balcon","patio","parrillero","pileta","piscina","quincho","seguridad","amenities","lavadero","terraza","baulera","club house","sum","gimnasio"]
    out=[]
    for k in kws:
        if re.search(k,text,re.I):
            out.append(k.replace("balcon","balcón").title())
    return out[:10]

def extract_property(url):
    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0 Chrome/126 Safari/537.36","Accept-Language":"es-AR,es;q=0.9"},timeout=20)
        r.raise_for_status()
        soup=BeautifulSoup(r.text,"html.parser")
        title=clean(soup.find("title").get_text() if soup.find("title") else "")
        desc=meta(soup,"description") or meta(soup,"og:description")
        text=" ".join([title,desc,clean(soup.get_text(" ",strip=True))[:9000]])
        return {
            "url":url,
            "title":title,
            "description":desc,
            "price":find_price(text),
            "property_type":find_type(text),
            "location":find_location(text),
            "bedrooms":find_number(text,[r"(\d+)\s*dorm",r"(\d+)\s*habitaci",r"(\d+)\s*amb"]),
            "bathrooms":find_number(text,[r"(\d+)\s*bañ",r"(\d+)\s*toilet"]),
            "surface":find_surface(text),
            "features":find_features(text),
            "source_status":"extracted"
        }
    except Exception as e:
        return {"url":url,"title":"","description":"","price":"Consultar precio","property_type":"Propiedad","location":"Ubicación a confirmar","bedrooms":"","bathrooms":"","surface":"","features":[],"source_status":f"fallback: {e}"}
