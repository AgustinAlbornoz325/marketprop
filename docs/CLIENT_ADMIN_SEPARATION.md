# v0.3.10.1 Client/Admin Separation

## Decisión
La administración de clientes no debe aparecer en el panel del cliente.

## Panel Cliente
El cliente/inmobiliaria solo ve:
- Generador
- Propiedades
- Contenidos
- Pipeline
- Calendario
- MarketDNA
- Métricas propias
- IG Ready / publicación cuando esté disponible

No ve:
- Lista de otras inmobiliarias
- Planes internos
- Facturación global
- Uso global de IA
- Roles globales
- Estado de suscripciones de otros clientes

## Panel Master Admin
El dueño de MarketProp ve:
- Clientes / inmobiliarias
- Usuarios
- Roles
- Planes
- Límites
- Facturación
- Estado de suscripción
- Uso de IA
- Control general

## Implementación v0.3.10.1
- Se mantiene backend multiworkspace.
- Se retira Workspace/Admin del panel cliente.
- Se crea `/admin/index.html` como panel separado.
- Próximo paso: auth real y protección del admin.
