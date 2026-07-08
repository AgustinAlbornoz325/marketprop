class PropertyAgent:
    def run(self, url: str) -> dict:
        u = url.lower()
        ptype = "Propiedad"
        if "casa" in u: ptype = "Casa"
        elif "departamento" in u or "depto" in u: ptype = "Departamento"
        elif "terreno" in u or "lote" in u: ptype = "Terreno"
        elif "local" in u: ptype = "Local"
        location = "Ubicación a confirmar"
        places = {"rosario":"Rosario", "funes":"Funes", "fisherton":"Fisherton", "pichincha":"Pichincha", "centro":"Centro", "alberdi":"Alberdi", "eche":"Echesortu"}
        for key, value in places.items():
            if key in u: location = value; break
        return {"url": url, "type": ptype, "location": location, "price": "Consultar precio", "detected_by": "PropertyAgent"}
