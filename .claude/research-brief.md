# Research Brief — Daily AI Researcher Agent

Este documento le dice al agente programado QUE buscar, COMO filtrar, y DONDE
guardar lo que encuentre. El agente lo lee al inicio de cada corrida.

## Audiencia final

Duenos de negocio y profesionales latinoamericanos que quieren entender e
implementar IA en sus empresas. No son tecnicos. Hablan espanol. Consumen
posts de LinkedIn (Growth para Profesionales).

## Fuentes a consultar

1. Lee `sources/news-sources.md` — extrae todas las URLs listadas bajo las
   secciones `## Newsletters`, `## Blogs / Labs oficiales`, `## Medios / Press`,
   `## Otras`.
2. Lee `sources/educational-sources.md` — extrae todas las URLs igual.
3. Ignora comentarios `<!-- ... -->`.

Si una seccion esta vacia, sigue con la siguiente. Si ambos archivos estan
completamente vacios, detente y escribe en el dump diario que no hay fuentes
configuradas.

## Categorias

Cada item que encuentres cae en una de dos categorias:

### `news` — va a `wiki/ai-news/`
Algo que PASO en el mundo de la IA:
- Lanzamientos de modelos (GPT, Claude, Gemini, Llama, DeepSeek, etc.)
- Anuncios de labs (Anthropic, OpenAI, Google DeepMind, Meta, xAI, etc.)
- Cambios regulatorios (EU AI Act, US executive orders, politicas nacionales)
- Movimientos de mercado (inversiones, adquisiciones, IPOs)
- Geopolitica IA (chip export controls, China, Taiwan)
- Benchmarks y papers con impacto (solo si tienen implicacion practica)

### `educational` — va a `wiki/ia-para-empresas/`
Como USAR IA en un negocio:
- Herramientas nuevas para SMBs (marketing, ventas, ops, HR, finanzas)
- How-tos y tutoriales paso a paso
- Prompts listos para usar
- Automatizaciones (Zapier, Make, n8n con IA)
- Casos de uso por industria (real estate, legal, health, education, e-comm)
- Frameworks para adopcion de IA
- Comparativas de tools

## Criterios de descarte

Descarta items que:
- Sean >48h viejos (chequea fecha de publicacion; si no hay fecha clara, asume
  que esta bien y avisa en el dump).
- Sean puro hype sin sustancia (titulares tipo "X va a revolucionar Y" sin
  detalle concreto).
- Sean papers academicos sin resumen accionable para no-tecnicos.
- Sean specs tecnicas profundas sin un "asi lo puedes usar".
- Ya aparezcan en los ultimos 7 dumps en `raw/daily/*.md` (mismo URL).

## Flujo del agente

1. Lee los dos `sources/*.md` y arma lista de URLs.
2. `WebFetch` cada URL. Para newsletters/blogs con archivo, extrae los 3-5
   posts mas recientes.
3. Filtra por fecha (ultimas 48h) y deduplica contra ultimos 7 dumps.
4. Clasifica cada item como `news` o `educational`.
5. Escribe el dump crudo en `raw/daily/YYYY-MM-DD.md` (formato abajo).
6. Por cada item, crea un articulo wiki en la carpeta correspondiente.
7. Actualiza `wiki/ai-news/_index.md` y `wiki/ia-para-empresas/_index.md`
   con los articulos nuevos.
8. NO tocar `wiki/ai/` (foundational). Solo cross-linkear hacia alli con
   `[[../ai/<topic>/<articulo>]]` cuando aplique.

## Formato del dump diario `raw/daily/YYYY-MM-DD.md`

```markdown
---
date: YYYY-MM-DD
sources_consulted: <numero>
items_found: <numero>
items_news: <numero>
items_educational: <numero>
---

# Daily Research — YYYY-MM-DD

## News

### [Titulo del articulo](URL)
- **Fuente**: Nombre de la fuente
- **Fecha**: YYYY-MM-DD
- **Resumen**: 3-5 bullets en espanol con los puntos clave
- **Angulo para duenos de negocio**: 1-2 lineas (por que les importa)
- **Wiki slug**: `ai-news/<slug-kebab-case>`

(repetir por cada item news)

## Educational

### [Titulo del articulo](URL)
- **Fuente**: Nombre de la fuente
- **Fecha**: YYYY-MM-DD
- **Categoria**: tool | how-to | caso de uso | prompt | automatizacion | framework
- **Resumen**: 3-5 bullets en espanol
- **Como implementarlo**: 1-2 lineas concretas
- **Wiki slug**: `ia-para-empresas/<slug-kebab-case>`

(repetir por cada item educational)

## Resumen para LinkedIn

Top 3 items con mejor hook para un post de LinkedIn (dueno de negocio latino):

1. **[Titulo]** — por que tiene hook: ...
2. **[Titulo]** — por que tiene hook: ...
3. **[Titulo]** — por que tiene hook: ...
```

## Formato de articulo wiki

Tanto en `wiki/ai-news/` como en `wiki/ia-para-empresas/`:

```markdown
# Titulo del articulo

Intro de 2-3 lineas: que es esto y por que importa.

## Contexto
Breve (3-5 bullets) que ubica la noticia o el tema.

## Que paso / De que se trata
Los detalles relevantes (5-8 bullets). Sin jerga tecnica innecesaria.

## Por que le importa a un dueno de negocio
2-4 bullets accionables. "Si tienes X tipo de negocio, esto significa Y."
Para articulos educational, aqui va el "como aplicarlo".

## Key Takeaways
- 3-5 takeaways cortos, cada uno una linea.

## Fuente
- [Titulo original](URL) — Nombre fuente — Fecha

## Cross-links
- [[../ai/ai-models/<slug>]] (si aplica)
- [[otros articulos del vault]]
```

## Volumen objetivo por dia

- 3-6 items `news`
- 2-4 items `educational`

Si una fuente no publico, esta bien saltar. Preferible poca calidad alta que
mucha baja.

## Estado y deduplicacion

No se usa un archivo de estado explicito. El agente deduplica leyendo los
ultimos 7 `raw/daily/*.md` y saltando URLs repetidas. Si el wiki slug ya existe,
no se sobreescribe — se agrega `-2` al slug o se actualiza el existente con
info nueva.

## Lo que el agente NO debe hacer

- NO hacer `WebSearch` libre. Solo `WebFetch` sobre URLs listadas en `sources/`.
- NO modificar `wiki/ai/` (foundational).
- NO crear carpetas nuevas fuera de `ai-news/` e `ia-para-empresas/`.
- NO escribir en `output/` (eso es para reportes de consultas, no para daily).
- NO borrar `raw/daily/*.md` antiguos (son historico para dedup).
