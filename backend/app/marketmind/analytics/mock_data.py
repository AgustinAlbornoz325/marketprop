COMMAND_CENTER = {
    "kpis": [
        {"label": "Contenido generado", "value": "128", "delta": "+24%", "detail": "Piezas creadas este mes"},
        {"label": "MarketMind Score", "value": "91", "delta": "+6", "detail": "Promedio de calidad"},
        {"label": "Propiedades activas", "value": "37", "delta": "+5", "detail": "Con contenido listo"},
        {"label": "Consultas estimadas", "value": "214", "delta": "+31%", "detail": "DMs / WhatsApp mock"},
    ],
    "quality": {"score": 87, "ready": 9, "blocked": 2},
    "alerts": [
        {"title": "Hook débil en Reel", "text": "Una pieza de Funes necesita primer segundo más fuerte.", "level": "warning"},
        {"title": "Meta Ads sin ángulo claro", "text": "El anuncio de inversión debe prometer consulta concreta.", "level": "danger"},
        {"title": "WhatsApp listo", "text": "3 mensajes están listos para enviar a prospectos.", "level": "success"},
    ],
    "insights": [
        {"title": "Dolor dominante", "text": "Los compradores preguntan primero por financiación y gastos iniciales."},
        {"title": "Objeción caliente", "text": "Dudan por zona antes que por precio."},
        {"title": "Frase reusable", "text": "¿Aceptan permuta o financiación?"},
        {"title": "Oportunidad", "text": "Crear contenido educativo sobre compra inicial y reservas."},
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
