# Real AI Connector

v0.3.5 conecta MarketMind con proveedores reales.

## Activar IA real
Copiar `backend/.env.example` a `backend/.env` y poner:

DEMO_MODE=false
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...

No es obligatorio cargar las tres claves. MarketMind usa la disponible.

## Endpoint
/api/marketmind/providers

## Seguridad
Nunca subir `.env` a GitHub.
