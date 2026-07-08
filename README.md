# MarketProp v0.3.2 Content Engine

Cambios:
- Hero más compacto.
- Agentes por plataforma: Facebook, Instagram, TikTok, WhatsApp, Mercado Libre y Meta Ads.
- Las variaciones cambian de verdad según estilo.
- TikTok genera hook + guion, no descripción genérica.
- WhatsApp suena humano.
- Mercado Libre es más técnico.
- Se agrega docs/AGENTE_COPY.md.

## Ejecutar
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html
