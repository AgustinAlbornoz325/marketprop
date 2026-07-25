# v0.3.12 Permissions Enforcement + UX Guardrails

## Objetivo
Que los permisos no sean solo visuales, sino reales en backend.

## Reglas principales

### super_admin
- Accede al Admin Master.
- Puede ver información global.
- Puede administrar clientes de MarketProp.

### owner
- Administra su inmobiliaria.
- Puede crear/eliminar propiedades.
- Puede crear pipeline/calendario/fuentes.
- No puede ver Admin Master global.

### admin
- Gestiona operación de la inmobiliaria.
- Puede crear propiedades, pipeline, calendario y fuentes.
- No puede eliminar datos críticos ni ver Admin Master.

### member
- Puede ver datos de su inmobiliaria.
- Puede generar y guardar contenido.
- No puede crear/eliminar propiedades base.
- No puede modificar fuentes MarketDNA.
- No puede administrar usuarios, planes ni facturación.

## Endpoints agregados
- GET `/api/data/permissions`

## Endpoints endurecidos
- POST `/api/data/properties`
- DELETE `/api/data/properties/{id}`
- POST `/api/data/pipeline`
- PATCH `/api/data/pipeline/{id}/status`
- POST `/api/data/calendar`
- POST `/api/data/sources`

## UX Guardrails
- La interfaz muestra el rol actual.
- Los botones sensibles se bloquean para usuarios sin permiso.
- Si el frontend falla, el backend igual responde 403.
