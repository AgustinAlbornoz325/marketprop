# MarketProp v0.3.9 SaaS Foundation Database

Versión acumulativa sobre v0.3.8.1.

## Qué cambia realmente

Esta versión empieza a convertir MarketProp de demo visual a estructura real de SaaS.

## Mantiene

- Command Center.
- Métricas de redes.
- Métricas inmobiliarias.
- Pipeline.
- Calendario.
- MarketDNA Sources.
- Generador.
- Botones de variación.
- Provider Gateway.
- MarketMind.
- Real AI Connector preparado.

## Agrega estructura real

- SQLite local.
- Modelos de datos.
- Schemas.
- Seed inicial.
- Endpoints CRUD.
- Pantalla Base real.

## Datos persistentes

Ahora se guardan localmente:

- Propiedades.
- Contenidos.
- Pipeline.
- Calendario.
- MarketDNA Sources.

La base se crea en:

backend/data/marketprop.db

## Ejecutar

cd backend
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn app.main:app --reload

Luego abrir frontend/index.html.

## Probar

Entrar a la pestaña Base real.
Apretar + Crear propiedad demo real.
Cerrar y volver a abrir. La propiedad debe seguir guardada.
