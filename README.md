# MarketProp v0.3.13 Usage Metering + Plan Limits

Versión acumulativa sobre v0.3.12.

## Mantiene
- Auth estable.
- Permisos reales.
- Admin Master.
- Panel cliente.
- Workspaces.
- Base real local.
- MarketMind.
- Command Center.
- Pipeline.
- Calendario.
- MarketDNA.
- IG Ready.

## Agrega
- Medición de uso por workspace.
- Límites por plan.
- Bloqueo por plan inactivo.
- Bloqueo por límite de contenidos.
- Bloqueo por créditos IA.
- Endpoint `/api/data/usage`.
- Nueva pestaña cliente: Uso / Plan.
- Admin Master con vista de uso por cliente.

## Qué se mide
- Contenidos generados.
- Créditos IA usados.
- Propiedades creadas.
- Pipeline creado.
- Calendario creado.
- Fuentes MarketDNA creadas.

## Credenciales demo

Admin Master:

admin@marketprop.com  
admin123

Cliente owner:

demo@marketprop.com  
123456

Empleado member:

empleado@marketprop.com  
123456

## Ejecutar

cd backend
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn app.main:app --reload

Luego abrir:

frontend/index.html

y también:

admin/index.html

## Guardar en Git

Commit recomendado:

MarketProp v0.3.13 Usage Metering Plan Limits

Tag:

v0.3.13
