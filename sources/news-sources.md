# AI News Sources

Fuentes curadas por Sebastian para el agente investigador diario.
Formato: `- [Nombre](URL) — descripcion corta`

El agente lee este archivo cada corrida y hace `WebFetch` sobre las URLs listadas.
Anadi fuentes nuevas simplemente anade una linea mas a la lista correspondiente.

## Blogs / Labs oficiales
- [Anthropic News](https://www.anthropic.com/news) — Anuncios oficiales de Anthropic (modelos, papers, partnerships, governance)
- [Google DeepMind Blog](https://deepmind.google/discover/blog/) — Gemini, Gemma, research releases, robotica

## Blogs de practitioners
- [Simon Willison's Weblog (Atom)](https://simonwillison.net/atom/everything/) — AI news + uso practico de LLMs, muy influyente en la comunidad

## Agregadores / Comunidad
- [Hacker News — AI stories (RSS)](https://hnrss.org/newest?q=AI) — Feed de HN filtrado por AI, noticias curadas por la comunidad

## Newsletters
<!-- Cuando encuentres newsletters que funcionen con WebFetch, anadelos aqui.
     NOTA: TechCrunch feeds y muchos Substacks bloquean WebFetch con 403. -->

## Notas
- Sitios que sabemos bloquean WebFetch con 403: techcrunch.com (RSS y HTML), substack.com (muchos feeds)
- Si una fuente nueva devuelve 403 repetidas veces, el agente la documenta en el dump diario y tu decides si la quitas
