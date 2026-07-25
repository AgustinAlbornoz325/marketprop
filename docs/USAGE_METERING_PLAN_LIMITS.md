# v0.3.13 Usage Metering + Plan Limits

## Objetivo
Medir uso real por workspace/inmobiliaria para preparar suscripciones y billing.

## Qué se mide
- Contenidos generados.
- Créditos IA usados.
- Propiedades creadas.
- Pipeline creado.
- Calendario creado.
- Fuentes MarketDNA creadas.

## Nuevos controles
- `assert_can_consume`
- `record_usage`
- `usage_snapshot`
- Endpoint `/api/data/usage`

## Límites actuales
Se leen desde `SubscriptionPlan`:
- monthly_content_limit
- ai_credit_limit
- seats_limit
- status

## Qué protege
- Si el plan no está activo, bloquea consumo.
- Si se supera el límite mensual de contenido, bloquea generación.
- Si se superan créditos IA, bloquea generación/variaciones.

## Nota
Todavía no hay pago real. Esto prepara la lógica para billing.
