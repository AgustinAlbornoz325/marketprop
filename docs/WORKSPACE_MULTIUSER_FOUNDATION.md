# v0.3.10 Workspace / Multiuser Foundation

## Objetivo
Preparar MarketProp para funcionar como SaaS multi-inmobiliaria.

## Se agrega
- Tabla `workspaces`.
- Tabla `user_accounts`.
- Tabla `subscription_plans`.
- Tabla `usage_events`.
- `workspace_id` en entidades centrales.
- Endpoints de workspace.
- Pestaña Workspace en frontend.
- Roles iniciales: owner, admin, member.
- Límites iniciales por plan.

## Importante
Esto todavía no es seguridad productiva final. Es la base estructural para que después cada inmobiliaria tenga sus datos separados, plan, usuarios y límites.
