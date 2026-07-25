# MarketProp v0.3.12 Permissions Enforcement + UX Guardrails

Versión acumulativa sobre v0.3.11.2.

## Mantiene
- Auth estable.
- Admin Master funcionando.
- Panel cliente funcionando.
- Separación cliente/admin.
- Base real local.
- Workspaces.
- MarketMind.
- Command Center.
- Pipeline.
- Calendario.
- MarketDNA.
- IG Ready.

## Agrega
- Permisos reales en backend.
- Endpoint `/api/data/permissions`.
- Validación por rol.
- UX guardrails en el panel cliente.
- Mensajes claros cuando un usuario no tiene permiso.
- Bloqueo real con error 403 si intenta ejecutar acciones sensibles.

## Roles

### super_admin
Dueño de MarketProp. Accede al Admin Master.

### owner
Dueño de una inmobiliaria cliente.

### admin
Administrador interno de una inmobiliaria.

### member
Usuario limitado. Puede generar contenido, pero no administrar datos base.

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

## Probar

1. Encender backend.
2. Entrar como `demo@marketprop.com`.
3. Revisar panel cliente.
4. Entrar como `empleado@marketprop.com`.
5. Verificar que no pueda crear datos base.
6. Abrir `admin/index.html`.
7. Entrar con `admin@marketprop.com`.
8. Verificar Admin Master.

## Ejecutar

cd backend
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn app.main:app --reload
