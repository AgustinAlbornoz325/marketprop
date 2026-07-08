# MarketMind Orchestrator

MarketMind es el cerebro de MarketProp.

## Qué hace
- Recibe la tarea del usuario.
- Interpreta la propiedad.
- Define estrategia de copy.
- Elige agente por plataforma.
- Elige modelo según la tarea.
- Evalúa calidad.
- Si la calidad es baja, regenera.
- Entrega contenido final.

## Estructura
backend/app/marketmind/
- orchestrator.py
- model_router.py
- evaluator.py
- memory.py
- agents/
- knowledge/
- providers/

## Nota
v0.3.3 usa proveedor mock para correr localmente sin API keys. El próximo sprint conecta GPT, Claude y Gemini.
