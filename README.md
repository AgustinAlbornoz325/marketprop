# MarketProp v0.3.3 MarketMind Orchestrator

Esta versión crea el cerebro base de MarketProp.

## Cambios
- Nuevo paquete `backend/app/marketmind/`.
- MarketMind Orchestrator coordina el flujo.
- ModelRouter decide qué modelo usar por tarea.
- Evaluator puntúa calidad.
- MemoryStore guarda eventos simples en runtime.
- Agentes por plataforma siguen separados.
- Endpoint `/api/marketmind/health`.

## Ejecutar
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html.

## Nota
Todavía no usa APIs reales de GPT, Claude o Gemini. Usa modo mock para que puedas correrlo localmente.
