# DECISIONS

001 - Hero definitivo: La IA hace todo el marketing. Vos vendé propiedades, ganá tiempo.
002 - Las descripciones deben estar impulsadas por agentes por plataforma.
003 - TikTok genera hook + guion, no descripción común.
004 - Mercado Libre prioriza claridad técnica.
005 - WhatsApp debe sonar humano.
006 - MarketMind será el cerebro que orquesta agentes y modelos.
007 - La plataforma no se casa con GPT, Claude ni Gemini. MarketMind elegirá por rendimiento.
008 - v0.3.3 crea la arquitectura real de orquestación con proveedor mock.

009 - v0.3.4 crea Provider Gateway para OpenAI, Claude, Gemini y mock local.
010 - MarketMind debe elegir proveedor por tarea, no por preferencia de marca.

009 - Antes de guardar v0.3.5 se corrigieron variaciones genéricas: cada botón debe cambiar estructura y enfoque real.

010 - Regla acumulativa: no se elimina lo que sirve; se consolida y se mejora.
011 - v0.3.6 consolida versiones anteriores antes de seguir.
012 - Se adopta la lógica útil del Command Center externo sin adoptar su diseño.
013 - El diseño MarketProp blanco/celeste se mantiene hasta el final salvo aprobación expresa.

010 - Hotfix v0.3.6.1: corregido import registry/provider_registry y await en rutas sync.

011 - v0.3.7: se mejora Command Center con métricas inmobiliarias sin cambiar diseño ni eliminar funciones.

012 - v0.3.8: se mejora Pipeline, Calendario y MarketDNA sin quitar funciones existentes.

013 - v0.3.8.1: hotfix acumulativo para restaurar métricas anteriores y logos/badges de redes sin quitar lo agregado en v0.3.8.

014 - v0.3.9: se inicia estructura real de SaaS con SQLite, persistencia local, entidades centrales y endpoints CRUD.

015 - v0.3.10: se agrega base multiworkspace, usuarios, roles, planes y usage events para preparar MarketProp como SaaS multi-inmobiliaria.

015 - v0.3.10.1: separación obligatoria entre panel cliente y panel master admin. Administración de clientes solo visible para Agustín/dueño de MarketProp.
