from sqlalchemy.orm import Session
from app.core.models import Workspace, UserAccount, SubscriptionPlan, Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource, UsageEvent
from app.core.security import hash_password

DEFAULT_WORKSPACE_ID = 1

def seed_database(db: Session):
    workspace = db.get(Workspace, DEFAULT_WORKSPACE_ID)
    if not workspace:
        workspace = Workspace(id=DEFAULT_WORKSPACE_ID, name="Forja Propiedades", slug="forja-propiedades", plan="Básico", status="active")
        db.add(workspace)
        db.flush()

    if not db.query(UserAccount).filter(UserAccount.email == "demo@marketprop.com").first():
        db.add(UserAccount(workspace_id=workspace.id, name="Agustín", email="demo@marketprop.com", password_hash=hash_password("123456"), role="owner", status="active"))

    if not db.query(SubscriptionPlan).filter(SubscriptionPlan.workspace_id == workspace.id).first():
        db.add(SubscriptionPlan(workspace_id=workspace.id, plan_name="Básico", status="trial", monthly_content_limit=500, ai_credit_limit=100000, seats_limit=2))

    if not db.query(Property).first():
        properties = [
            Property(workspace_id=workspace.id, title="Casa premium en Funes", url="https://www.ejemplo.com/casa-premium-funes", location="Funes", property_type="Casa", price="USD 180.000", notes="Propiedad demo real persistente."),
            Property(workspace_id=workspace.id, title="Departamento Rosario Centro", url="https://www.ejemplo.com/depto-rosario-centro", location="Rosario Centro", property_type="Departamento", price="USD 85.000", notes="Ideal para contenido de visita."),
            Property(workspace_id=workspace.id, title="Terreno Fisherton", url="https://www.ejemplo.com/terreno-fisherton", location="Fisherton", property_type="Terreno", price="USD 95.000", notes="Ángulo inversor."),
        ]
        db.add_all(properties)
        db.flush()

        db.add_all([
            PipelineItem(workspace_id=workspace.id, property_title="Casa premium en Funes", platform="Instagram/TikTok", format="Reel", objective="Generar consultas calificadas", status="Contenido generado", owner="Agus", score=94, next_action="Revisar hook y publicar", blocker="Sin bloqueo", source="Link de propiedad"),
            PipelineItem(workspace_id=workspace.id, property_title="Departamento Rosario Centro", platform="WhatsApp", format="Mensaje", objective="Agendar visita", status="Aprobado", owner="Agus", score=91, next_action="Enviar a interesados", blocker="Sin bloqueo", source="Contenido generado"),
            PipelineItem(workspace_id=workspace.id, property_title="Terreno Fisherton", platform="Instagram", format="Carrusel", objective="Captar inversores", status="Revisión pendiente", owner="Equipo", score=78, next_action="Agregar argumento de rentabilidad", blocker="CTA flojo", source="MarketDNA"),
        ])

        db.add_all([
            CalendarItem(workspace_id=workspace.id, day="Lun", time="10:00", title="Reel: casa premium en Funes", platform="Instagram/TikTok", property_title="Casa premium en Funes", goal="Alcance + DM", score=92),
            CalendarItem(workspace_id=workspace.id, day="Mié", time="11:00", title="WhatsApp: departamento Rosario", platform="WhatsApp", property_title="Departamento Rosario Centro", goal="Agendar visita", score=91),
            CalendarItem(workspace_id=workspace.id, day="Vie", time="12:30", title="Carrusel: terreno Fisherton", platform="Instagram", property_title="Terreno Fisherton", goal="Inversores", score=88),
        ])

        db.add_all([
            MarketDNASource(workspace_id=workspace.id, name="Publicaciones anteriores", source_type="Historial de contenido", status="Activo mock", value="Detecta tono, CTAs y hooks que mejor funcionan.", signals="CTA ganador: te paso más info, Mejor formato: Reel"),
            MarketDNASource(workspace_id=workspace.id, name="Consultas WhatsApp", source_type="Fuente comercial", status="Mock", value="Convierte preguntas frecuentes en ideas de contenido.", signals="¿Sigue disponible?, ¿Se puede visitar?, ¿Acepta entrega?"),
            MarketDNASource(workspace_id=workspace.id, name="Quality Gate", source_type="Reglas MarketMind", status="Activo", value="Evalúa hook, claridad, CTA y adaptación por red.", signals="hook, claridad, CTA, originalidad"),
        ])

        db.add_all([
            ContentItem(workspace_id=workspace.id, property_id=1, platform="Instagram", format="Reel", style="premium", title="Casa premium en Funes", body="Una casa pensada para vivir Funes con comodidad, diseño y ubicación estratégica. Escribime y te paso más info.", score=91, status="Contenido generado"),
            ContentItem(workspace_id=workspace.id, property_id=2, platform="WhatsApp", format="Mensaje directo", style="humano", title="Depto Rosario Centro", body="Hola, tengo un departamento en Rosario Centro que puede encajar con lo que buscabas. ¿Querés que te pase fotos y detalles?", score=88, status="Aprobado"),
        ])

        db.add_all([
            UsageEvent(workspace_id=workspace.id, event_type="content_generated", amount=128, meta="seed"),
            UsageEvent(workspace_id=workspace.id, event_type="ai_credits_used", amount=3400, meta="seed"),
        ])

    db.commit()
