# v0.3.8 Pipeline + Calendario + MarketDNA

## Objetivo
Mejorar la capa operativa de MarketProp sin quitar funciones existentes.

## Agregado
- Pipeline más detallado con próxima acción, fuente, bloqueo y score.
- Calendario editorial más claro por día, horario, plataforma, objetivo y propiedad.
- MarketDNA Sources con estado, valor y señales.
- Nuevos endpoints:
  - /api/analytics/pipeline-detail
  - /api/analytics/calendar-detail
  - /api/analytics/marketdna-sources-detail

## Regla
Se mantiene diseño MarketProp. Se usa la lógica útil del dashboard externo sin copiar su diseño.
