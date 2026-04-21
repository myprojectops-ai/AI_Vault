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

## Daily Research (Scheduled Agent)

- Un agente programado corre lun-vie y hace research diario de IA a partir
  de fuentes curadas por Sebastian.
- Lee `.claude/research-brief.md` para las reglas de filtrado, clasificacion
  y formato de output.
- Lee `sources/news-sources.md` y `sources/educational-sources.md` para saber
  que URLs consultar. No hace WebSearch libre — solo WebFetch sobre esas URLs.
- Escribe el dump crudo del dia en `raw/daily/YYYY-MM-DD.md`.
- Compila articulos a `wiki/ai-news/` (noticias) y `wiki/ia-para-empresas/`
  (contenido educativo practico para duenos de negocio).
- `wiki/ai/` es foundational knowledge — cross-linkear hacia alli con
  `[[../ai/...]]` cuando aplique, pero NO anadir contenido nuevo alli.
- El proposito ultimo del material es alimentar posts de LinkedIn de
  Growth para Profesionales.
