COMMAND_CENTER = {
    "kpis": [
        {"label": "Contenido generado", "value": "128", "delta": "+24%", "detail": "Piezas creadas este mes"},
        {"label": "MarketMind Score", "value": "91", "delta": "+6", "detail": "Promedio de calidad"},
        {"label": "Propiedades activas", "value": "37", "delta": "+5", "detail": "Con contenido listo"},
        {"label": "Consultas estimadas", "value": "214", "delta": "+31%", "detail": "DMs / WhatsApp mock"},
        {"label": "Visitas agendadas", "value": "26", "delta": "+12%", "detail": "Objetivo comercial final"},
        {"label": "Costo IA estimado", "value": "US$ 3.42", "delta": "-18%", "detail": "Control de consumo mensual"},
        {"label": "Hooks aprobados", "value": "89%", "delta": "+9", "detail": "Pasan Quality Gate"},
        {"label": "Contenido reciclable", "value": "42", "delta": "+16", "detail": "Piezas reutilizables"}
    ],
    "quality": {
        "score": 87,
        "ready": 9,
        "blocked": 2,
        "weak_hooks": 3,
        "weak_cta": 1,
        "needs_property_data": 4
    },
    "funnel": [
        {"label": "Alcance", "value": "48.2K", "pct": 100},
        {"label": "Visitas perfil", "value": "6.7K", "pct": 72},
        {"label": "Clicks / WhatsApp", "value": "812", "pct": 46},
        {"label": "DMs", "value": "214", "pct": 31},
        {"label": "Visitas agendadas", "value": "26", "pct": 18}
    ],
    "format_reach": [
        {"label": "Reels", "value": 92, "detail": "mejor para alcance"},
        {"label": "Stories", "value": 64, "detail": "mejor para confianza"},
        {"label": "Carruseles", "value": 58, "detail": "mejor educativo"},
        {"label": "Meta Ads", "value": 49, "detail": "mejor leads"},
        {"label": "WhatsApp", "value": 71, "detail": "mejor cierre"}
    ],
    "property_signals": [
        {"title": "Casa premium en Funes", "signal": "Más guardados", "score": 94, "action": "Crear Reel + Meta Ad"},
        {"title": "Departamento Rosario Centro", "signal": "Más DMs", "score": 91, "action": "Enviar WhatsApp directo"},
        {"title": "Terreno Fisherton", "signal": "Interés inversor", "score": 88, "action": "Crear carrusel de rentabilidad"},
        {"title": "Monoambiente Centro", "signal": "Consulta por financiación", "score": 84, "action": "Crear pieza educativa"}
    ],
    "weekly_slots": [
        {"day": "Lun", "hour": "10:00", "score": 88},
        {"day": "Mar", "hour": "18:00", "score": 76},
        {"day": "Mié", "hour": "12:00", "score": 91},
        {"day": "Jue", "hour": "20:00", "score": 82},
        {"day": "Vie", "hour": "11:00", "score": 79},
        {"day": "Sáb", "hour": "19:00", "score": 69},
        {"day": "Dom", "hour": "20:30", "score": 73}
    ],
    "alerts": [
        {"title": "Hook débil en Reel", "text": "La pieza de Funes necesita primer segundo más fuerte.", "level": "warning"},
        {"title": "Meta Ads sin ángulo claro", "text": "El anuncio de inversión debe prometer consulta concreta.", "level": "danger"},
        {"title": "WhatsApp listo", "text": "3 mensajes están listos para enviar a prospectos.", "level": "success"},
        {"title": "Propiedad sin datos", "text": "4 contenidos necesitan precio, barrio o características para mejorar el score.", "level": "warning"}
    ],
    "insights": [
        {"title": "Dolor dominante", "text": "Los compradores preguntan primero por financiación y gastos iniciales."},
        {"title": "Objeción caliente", "text": "Dudan por zona antes que por precio."},
        {"title": "Frase reusable", "text": "¿Aceptan permuta o financiación?"},
        {"title": "Oportunidad", "text": "Crear contenido educativo sobre compra inicial y reservas."},
        {"title": "Siguiente acción", "text": "Convertir la mejor propiedad de la semana en campaña multired."},
        {"title": "Aprendizaje MarketDNA", "text": "Los CTAs con 'te paso más info' convierten mejor que 'consultá'."}
    ]
}

PIPELINE = [
    {"status": "Propiedad cargada", "format": "Casa", "platform": "Todas", "property": "Casa premium en Funes", "objective": "DM", "score": 94, "owner": "Agus"},
    {"status": "Contenido generado", "format": "Reel", "platform": "TikTok", "property": "Departamento en Rosario", "objective": "Agendar visita", "score": 88, "owner": "Agus"},
    {"status": "Revisión pendiente", "format": "Carrusel", "platform": "Instagram", "property": "Terreno en Fisherton", "objective": "Inversor", "score": 76, "owner": "Equipo"},
    {"status": "Aprobado", "format": "Mensaje", "platform": "WhatsApp", "property": "Monoambiente Centro", "objective": "Consulta", "score": 91, "owner": "Agus"},
    {"status": "Publicado", "format": "Ad", "platform": "Meta Ads", "property": "Casa Fisherton", "objective": "Lead", "score": 84, "owner": "Equipo"},
    {"status": "Midiendo", "format": "Post", "platform": "Facebook", "property": "Lote Funes", "objective": "DM", "score": 86, "owner": "Agus"},
]

CALENDAR = [
    {"day": "Lun", "time": "10:00", "title": "Reel: casa premium en Funes", "platform": "Instagram/TikTok"},
    {"day": "Mar", "time": "18:00", "title": "Stories: encuesta financiación", "platform": "Instagram"},
    {"day": "Mié", "time": "12:00", "title": "Carrusel: inversión en terrenos", "platform": "Instagram"},
    {"day": "Jue", "time": "20:00", "title": "Meta Ad: departamento Rosario", "platform": "Meta Ads"},
    {"day": "Vie", "time": "11:00", "title": "WhatsApp broadcast propietarios", "platform": "WhatsApp"},
]

SOURCES = [
    {"name": "Publicaciones anteriores", "type": "MarketDNA", "summary": "Aprende tono, hooks y CTAs de la inmobiliaria.", "tags": ["marca", "tono", "historial"]},
    {"name": "DMs de Instagram", "type": "Futuro conector", "summary": "Detecta preguntas repetidas y objeciones reales.", "tags": ["objeciones", "DM", "Meta"]},
    {"name": "Consultas WhatsApp", "type": "Fuente comercial", "summary": "Convierte preguntas frecuentes en contenido.", "tags": ["leads", "ventas", "preguntas"]},
    {"name": "Banco de hooks inmobiliarios", "type": "Curado", "summary": "Patrones por zona, precio, urgencia e inversión.", "tags": ["hooks", "viralidad", "MarketMind"]},
    {"name": "Videos virales", "type": "Escaneo Videos", "summary": "Inspira formatos sin copiar contenido.", "tags": ["reels", "tiktok", "patrones"]},
    {"name": "Quality Gate", "type": "Reglas", "summary": "Evalúa claridad, CTA, plataforma y originalidad.", "tags": ["score", "calidad", "bloqueo"]},
]
