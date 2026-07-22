# MarketProp SaaS Architecture

## Capas actuales

1. Frontend local estático.
2. Backend FastAPI.
3. Base SQLite local.
4. Workspace / usuario / plan preparados.
5. Datos persistentes separados por `workspace_id`.

## Próximas capas profesionales

1. Auth real con tokens JWT y refresh tokens.
2. Permisos por rol.
3. PostgreSQL online.
4. Billing y suscripciones.
5. Deploy staging.
6. Logs, backups y monitoreo.
7. Conectores reales.
