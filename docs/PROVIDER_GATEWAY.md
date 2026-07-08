# Provider Gateway

MarketMind no depende de una sola IA.

## Proveedores preparados
- OpenAI / GPT: `OPENAI_API_KEY`
- Anthropic / Claude: `ANTHROPIC_API_KEY`
- Google / Gemini: `GOOGLE_API_KEY` o `GEMINI_API_KEY`
- Mock local: siempre disponible

## Cómo funciona
1. El usuario pide contenido.
2. MarketMind identifica la tarea.
3. ModelRouter revisa proveedores disponibles.
4. Elige el proveedor/modelo por tarea.
5. Si no hay API keys, usa mock local.

## Regla importante
MarketProp no se casa con ningún proveedor. El producto es MarketMind. GPT, Claude y Gemini son motores intercambiables.

## Próximo sprint
Activar llamadas reales a APIs externas con variables de entorno.
