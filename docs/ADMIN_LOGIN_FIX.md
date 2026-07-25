# v0.3.11.1 Admin Login Fix

## Error detectado
En `admin/index.html` aparecía:

`Cannot read properties of undefined (reading 'add')`

## Causa
Choque de nombre entre el elemento del DOM `adminLogin` y la función `adminLogin()`.

## Corrección
- Elemento visual: `adminLoginScreen`.
- Función: `doAdminLogin()`.
- Acceso a DOM mediante `document.getElementById`.

## Regla
No se toca el panel cliente ni la lógica de Auth. Solo se corrige el login del panel Admin Master.
