import re,requests
from bs4 import BeautifulSoup
def clean(t): return re.sub(r"\s+"," ",t or "").strip()
def meta(s,n):
    tag=s.find("meta",attrs={"name":n}) or s.find("meta",attrs={"property":n})
    return clean(tag.get("content")) if tag and tag.get("content") else ""
def price(t):
    for p,pre in [(r"USD\s?[\$]?\s?([\d\.\,]+)","USD"),(r"U\$S\s?([\d\.\,]+)","USD"),(r"\$\s?([\d\.\,]+)","$")]:
        m=re.search(p,t,re.I)
        if m: return f"{pre} {m.group(1)}"
    return "Consultar precio"
def ptype(t):
    x=t.lower()
    if "terreno" in x or "lote" in x: return "Terreno"
    if "casa" in x: return "Casa"
    if "departamento" in x or "depto" in x: return "Departamento"
    return "Propiedad"
def loc(t):
    places=["Rosario","Funes","Echesortu","Fisherton","Centro","Pichincha","Alberdi","Puerto Norte","Vida Jardín","Santa Fe"]
    f=[p for p in places if re.search(p,t,re.I)]
    return " · ".join(dict.fromkeys(f[:2])) if f else "Ubicación a confirmar"
def num(t,patterns):
    for p in patterns:
        m=re.search(p,t,re.I)
        if m: return m.group(1)
    return ""
def surf(t):
    for p in [r"(\d+[\,\.]?\d*)\s*m2",r"(\d+[\,\.]?\d*)\s*m²"]:
        m=re.search(p,t,re.I)
        if m: return f"{m.group(1)} m²"
    return ""
def feats(t):
    kws=["cochera","balcón","balcon","patio","parrillero","pileta","piscina","quincho","seguridad","amenities","lavadero","terraza"]
    return [k.replace("balcon","balcón").title() for k in kws if re.search(k,t,re.I)][:10]
def extract_property(url):
    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0 Chrome/126 Safari/537.36"},timeout=20)
        r.raise_for_status(); soup=BeautifulSoup(r.text,"html.parser")
        title=clean(soup.find("title").get_text() if soup.find("title") else "")
        desc=meta(soup,"description") or meta(soup,"og:description")
        text=" ".join([title,desc,clean(soup.get_text(" ",strip=True))[:9000]])
        return {"url":url,"title":title,"description":desc,"price":price(text),"property_type":ptype(text),"location":loc(text),"bedrooms":num(text,[r"(\d+)\s*dorm",r"(\d+)\s*amb"]),"bathrooms":num(text,[r"(\d+)\s*bañ"]),"surface":surf(text),"features":feats(text),"source_status":"extracted"}
    except Exception as e:
        return {"url":url,"title":"","description":"","price":"Consultar precio","property_type":"Propiedad","location":"Ubicación a confirmar","bedrooms":"","bathrooms":"","surface":"","features":[],"source_status":f"fallback: {e}"}
