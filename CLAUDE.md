## Knowledge Base Rules

- This is an LLM-maintained knowledge base. You are the librarian.
- The wiki/ folder is YOUR domain — you write and maintain everything in it.
  I rarely edit wiki files directly.
- raw/ is the inbox. When I dump files here, you process them into the wiki
  during a "compile" step.
- wiki/_master-index.md is the entry point. It lists every topic folder with
  a one-line description. Always keep this up to date.
- Each topic gets its own subfolder in wiki/ (e.g., wiki/ai-agents/) with its
  own _index.md that lists all articles in that topic with brief descriptions.
- Always use [[wiki links]] to connect related concepts across topics.
- When compiling raw material:
  1. Read the raw file
  2. Decide which topic it belongs to (or create a new one)
  3. Write a wiki article with key takeaways and relevant links
  4. Update that topic's _index.md
  5. Update wiki/_master-index.md
  6. If a raw file spans multiple topics, create articles in both and cross-link
- Keep articles concise — bullet points over paragraphs.
- Include a ## Key Takeaways section in every wiki article.
- output/ is for query results and generated reports.
- When answering questions, read _master-index.md first to navigate, then
  drill into the relevant topic _index.md, then read specific articles.
- When I ask you to "compile", process everything in raw/ that hasn't been
  compiled yet into the wiki.
- When I ask you to "audit" or "lint", review the wiki for inconsistencies,
  broken links, gaps, and suggest improvements.

## Daily Research (GitHub Action)

Un workflow de GitHub Actions corre lun-vie a las 13:30 UTC (8:30am Bogota)
y hace research diario de IA a partir de fuentes curadas.

**Arquitectura:**
- Workflow: `.github/workflows/daily-research.yml` (cron en GH infra)
- Script: `scripts/daily_research.py` (Python: fetch + filter + dedup + Claude API)
- Requiere secret `ANTHROPIC_API_KEY` en repo settings

**Flujo:**
1. Lee URLs desde `sources/news-sources.md` y `sources/educational-sources.md`
   (ignora comentarios HTML).
2. Fetch via `feedparser` (RSS/Atom) con user-agent propio.
3. Filtra por fecha (ultimas 48h) y dedup contra `raw/daily/*.md` de los
   ultimos 7 dias.
4. Llama a Claude UNA VEZ con todos los items: clasifica (news/educational/skip),
   genera titulo, slug, bullets, angulo para negocio, y articulo wiki completo.
5. Escribe articulos en `wiki/ai-news/` o `wiki/ia-para-empresas/`.
6. Actualiza `_index.md` de cada seccion con los nuevos articulos.
7. Escribe `raw/daily/YYYY-MM-DD.md` con resumen y top-3 para LinkedIn.
8. Commit + push con el `GITHUB_TOKEN` built-in de GH Actions.

**Reglas:**
- `wiki/ai/` es foundational knowledge — el script NO lo toca. Los articulos
  nuevos solo cross-linkean hacia alli con `[[../ai/...]]` cuando aplique.
- `.claude/research-brief.md` es el spec vigente (audiencia, criterios de
  clasificacion, formato de articulos). El prompt del script lo refleja.
- El proposito ultimo del material es alimentar posts de LinkedIn de
  Growth para Profesionales.

**Trigger manual:** via GH UI (`Actions` tab → `Daily AI Research` → `Run workflow`)
o via `gh workflow run daily-research.yml`.

**Sistema legacy (deshabilitado):** habia un scheduled agent en claude.ai
(`trig_011kNM3YzqXqjNwmDvd7Vozy`) que se descartó porque el entorno remoto
bloqueaba WebFetch a nivel de red. Queda deshabilitado como historia.
