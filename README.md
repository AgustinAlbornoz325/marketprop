# MarketProp v0.3.10.1 Client/Admin Separation

Hotfix profesional sobre v0.3.10.

## Decisión central

La administración de clientes, usuarios, planes, límites y facturación no debe aparecer en el panel del cliente.

## Panel Cliente

Abrir:

frontend/index.html

El cliente ve solo herramientas de marketing:
- Generador
- Command Center
- Propiedades / base real
- Pipeline
- Calendario
- MarketDNA
- IG Ready

## Panel Master Admin

Abrir:

admin/index.html

Solo para el dueño de MarketProp. Permite administrar:
- Clientes / inmobiliarias
- Usuarios
- Roles
- Planes
- Límites
- Facturación
- Uso de IA
- Seguridad

## Backend

Se mantiene la base multiworkspace de v0.3.10 porque es necesaria para una SaaS real, pero no se muestra en el panel del cliente.

## Próximo paso

v0.3.11 Auth + Roles + Permissions

Objetivo:
- Login real.
- Proteger panel admin.
- Proteger panel cliente.
- Diferenciar dueño/admin/cliente.
