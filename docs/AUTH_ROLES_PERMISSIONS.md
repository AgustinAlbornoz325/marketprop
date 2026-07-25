# v0.3.11 Auth + Roles + Permissions

## Objetivo
Convertir la separación cliente/admin en una estructura de acceso más real.

## Roles
- super_admin: dueño de MarketProp. Accede al Admin Master.
- owner: dueño de una inmobiliaria cliente. Accede al panel cliente.
- admin: administrador interno de una inmobiliaria.
- member: empleado o usuario limitado de una inmobiliaria.

## Credenciales demo locales
- Admin Master:
  - admin@marketprop.com
  - admin123
- Cliente demo:
  - demo@marketprop.com
  - 123456
- Empleado demo:
  - empleado@marketprop.com
  - 123456

## Qué se agrega
- Tokens firmados con HMAC.
- Endpoint /api/auth/me.
- Login sin fallback silencioso.
- Panel admin protegido por rol super_admin.
- Endpoint /api/admin/overview protegido.
- Panel cliente sin administración global visible.
- Headers Authorization en frontend.

## Qué todavía no es producción final
- No hay recuperación de contraseña.
- No hay email verification.
- No hay sesiones revocables.
- No hay 2FA.
- No hay billing real.

## Próximo paso sugerido
v0.3.12: Permissions Enforcement + UX Polish.
