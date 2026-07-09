# MarketProp v0.3.7 Command Center Polish

Versión acumulativa sobre v0.3.6.1.

## Mantiene
- MarketMind Orchestrator
- Provider Gateway
- Real AI Connector
- Button QA Fix
- Agentes por plataforma
- Command Center
- Pipeline
- Calendario
- MarketDNA Sources
- IG Ready
- Módulos legacy preservados

## Mejora
- Command Center más profesional.
- Métricas adaptadas al rubro inmobiliario.
- Funnel comercial.
- Señales por propiedad.
- Quality Gate más claro.
- Alertas e insights más accionables.

## Ejecutar
cd backend
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html.
