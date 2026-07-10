from sqlalchemy.orm import Session
from app.core.models import Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource

def seed_database(db: Session):
    if db.query(Property).first():
        return
    db.add_all([
        Property(title="Casa premium en Funes", url="https://www.ejemplo.com/casa-premium-funes", location="Funes", property_type="Casa", price="USD 180.000", notes="Propiedad demo persistente."),
        Property(title="Departamento Rosario Centro", url="https://www.ejemplo.com/depto-rosario-centro", location="Rosario Centro", property_type="Departamento", price="USD 85.000", notes="Ideal para agendar visita."),
        Property(title="Terreno Fisherton", url="https://www.ejemplo.com/terreno-fisherton", location="Fisherton", property_type="Terreno", price="USD 95.000", notes="Ángulo inversor."),
    ])
    db.flush()
    db.add_all([
        ContentItem(property_id=1, platform="Instagram", format="Reel", style="premium", title="Casa premium en Funes", body="Una casa pensada para vivir Funes con comodidad, diseño y ubicación estratégica. Escribime y te paso más info.", score=91, status="Contenido generado"),
        ContentItem(property_id=2, platform="WhatsApp", format="Mensaje directo", style="humano", title="Depto Rosario Centro", body="Hola, tengo un departamento en Rosario Centro que puede encajar con lo que buscabas. ¿Querés que te pase fotos y detalles?", score=88, status="Aprobado"),
    ])
    db.add_all([
        PipelineItem(property_title="Casa premium en Funes", platform="Instagram/TikTok", format="Reel", objective="Generar consultas calificadas", status="Contenido generado", owner="Agus", score=94, next_action="Revisar hook y publicar", blocker="Sin bloqueo", source="Link de propiedad"),
        PipelineItem(property_title="Departamento Rosario Centro", platform="WhatsApp", format="Mensaje", objective="Agendar visita", status="Aprobado", owner="Agus", score=91, next_action="Enviar a interesados", blocker="Sin bloqueo", source="Contenido generado"),
        PipelineItem(property_title="Terreno Fisherton", platform="Instagram", format="Carrusel", objective="Captar inversores", status="Revisión pendiente", owner="Equipo", score=78, next_action="Agregar argumento de rentabilidad", blocker="CTA flojo", source="MarketDNA"),
    ])
    db.add_all([
        CalendarItem(day="Lun", time="10:00", title="Reel: casa premium en Funes", platform="Instagram/TikTok", property_title="Casa premium en Funes", goal="Alcance + DM", score=92),
        CalendarItem(day="Mié", time="11:00", title="WhatsApp: departamento Rosario", platform="WhatsApp", property_title="Departamento Rosario Centro", goal="Agendar visita", score=91),
        CalendarItem(day="Vie", time="12:30", title="Carrusel: terreno Fisherton", platform="Instagram", property_title="Terreno Fisherton", goal="Inversores", score=88),
    ])
    db.add_all([
        MarketDNASource(name="Publicaciones anteriores", source_type="Historial de contenido", status="Activo mock", value="Detecta tono, CTAs y hooks que mejor funcionan.", signals="CTA ganador: te paso más info, Mejor formato: Reel"),
        MarketDNASource(name="Consultas WhatsApp", source_type="Fuente comercial", status="Mock", value="Convierte preguntas frecuentes en ideas de contenido.", signals="¿Sigue disponible?, ¿Se puede visitar?, ¿Acepta entrega?"),
        MarketDNASource(name="Quality Gate", source_type="Reglas MarketMind", status="Activo", value="Evalúa hook, claridad, CTA y adaptación por red.", signals="hook, claridad, CTA, originalidad"),
    ])
    db.commit()
