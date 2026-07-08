# MarketProp v0.3.4 Provider Gateway

Esta versión prepara MarketMind para usar distintos proveedores de IA.

## Cambios principales
- Provider Gateway creado.
- ModelRouter detecta proveedores disponibles.
- Preparado para OpenAI, Anthropic/Claude y Google/Gemini.
- Modo mock local si no hay API keys.
- Endpoint `/api/marketmind/providers`.
- MarketMind muestra proveedor + modelo elegido por tarea.

## Ejecutar
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html.

## API keys opcionales
En esta versión no son obligatorias.
Próximo sprint: llamadas reales.
