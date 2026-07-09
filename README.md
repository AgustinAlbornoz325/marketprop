# MarketProp v0.3.6.1 Backend Hotfix

Hotfix sobre v0.3.6 Consolidated Command Center.

## Arreglos
- Corrige import de `registry` en providers.
- Corrige llamadas del backend para que no usen `await` sobre métodos sync.
- Mantiene todo lo consolidado de v0.3.6:
  - MarketMind Orchestrator
  - Provider Gateway
  - Real AI Connector
  - Button QA Fix
  - Command Center
  - Pipeline
  - Calendario
  - MarketDNA Sources
  - IG Ready

## Ejecutar
cd backend
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html.
