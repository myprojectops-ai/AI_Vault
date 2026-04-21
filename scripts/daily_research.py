#!/usr/bin/env python3
"""Daily AI research pipeline.

Reads curated sources from sources/*.md, fetches RSS/Atom feeds, filters by
date, dedupes against past dumps, classifies items via Claude API, writes
wiki articles and a daily dump. Designed to run in GitHub Actions.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
from anthropic import Anthropic
from dateutil import parser as dateparser

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = REPO_ROOT / "sources"
RAW_DAILY = REPO_ROOT / "raw" / "daily"
WIKI_NEWS = REPO_ROOT / "wiki" / "ai-news"
WIKI_EDU = REPO_ROOT / "wiki" / "ia-para-empresas"

FETCH_WINDOW_HOURS = 48
DEDUP_LOOKBACK_DAYS = 7
MAX_ITEMS_PER_DAY = 12
CLAUDE_MODEL = "claude-sonnet-4-6"

URL_IN_MD = re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

client = Anthropic()


def load_source_urls(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    text = HTML_COMMENT.sub("", path.read_text(encoding="utf-8"))
    return URL_IN_MD.findall(text)


def fetch_feed(url: str) -> tuple[list[dict], str | None]:
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "AI-Vault-Researcher/1.0 (+https://github.com/myprojectops-ai/AI_Vault)"},
            timeout=25,
        )
        resp.raise_for_status()
    except Exception as e:
        return [], f"fetch failed: {e}"

    feed = feedparser.parse(resp.text)
    if not feed.entries:
        return [], "not parseable as RSS/Atom"

    items = []
    for e in feed.entries[:10]:
        items.append({
            "title": (e.get("title") or "").strip(),
            "url": e.get("link") or "",
            "published": e.get("published") or e.get("updated") or "",
            "summary": (e.get("summary") or e.get("description") or "")[:2000],
        })
    return items, None


def is_recent(pub_str: str, hours: int) -> bool:
    if not pub_str:
        return True
    try:
        dt = dateparser.parse(pub_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) - dt < timedelta(hours=hours)
    except Exception:
        return True


def load_seen_urls(lookback_days: int) -> set[str]:
    urls: set[str] = set()
    if not RAW_DAILY.exists():
        return urls
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    for f in RAW_DAILY.glob("*.md"):
        try:
            fdate = datetime.strptime(f.stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if fdate < cutoff:
                continue
        except ValueError:
            continue
        text = f.read_text(encoding="utf-8")
        for _, url in URL_IN_MD.findall(text):
            urls.add(url)
    return urls


def classify_and_compile(items: list[dict]) -> list[dict]:
    """Single Claude API call that classifies + drafts wiki articles for all items."""
    payload = [
        {"idx": i, "title": it["title"], "url": it["url"], "source": it.get("source_name", ""),
         "published": it.get("published", ""), "summary": it.get("summary", "")}
        for i, it in enumerate(items)
    ]

    prompt = f"""You are curating AI content for a Latin American business-owner audience on LinkedIn (Growth para Profesionales).

For each item below, return a JSON object with:
- idx: the item index (int)
- category: "news" | "educational" | "skip"
    * news = something that happened: model launches, lab announcements, regulation, market moves
    * educational = how to use AI in a business: tools, how-tos, prompts, automations, case studies, frameworks
    * skip = pure hype, irrelevant to business owners, too technical with no applied angle
- slug: kebab-case slug, 3-6 words, in Spanish or English matching the title
- clean_title: concise title (Spanish preferred if translation makes sense; keep English for proper nouns / tech terms)
- business_angle: 1-2 sentences in Spanish explaining why a non-technical business owner should care
- summary_bullets: array of 3-5 short Spanish bullets summarizing the key points
- wiki_article: full markdown article in Spanish with this exact structure:

# {{clean_title}}

{{2-3 line intro in Spanish}}

## Contexto
- bullet
- bullet
- bullet

## Que paso / De que se trata
- bullet (5-8 bullets, no jargon)
- bullet

## Por que le importa a un dueno de negocio
- bullet accionable (2-4 bullets)
- bullet accionable

## Key Takeaways
- 3-5 one-line takeaways

## Fuente
- [{{title}}]({{url}}) — {{source}} — {{date}}

Do not include classification of "skip" in wiki_article (use empty string "" for skip items). For valid items, write real content — no "TODO" or placeholders.

Input items (JSON):
{json.dumps(payload, ensure_ascii=False)}

Respond with a JSON array only. No prose, no code fences."""

    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    # strip code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    enriched = json.loads(text)

    by_idx = {e["idx"]: e for e in enriched}
    out = []
    for i, it in enumerate(items):
        extra = by_idx.get(i)
        if not extra:
            continue
        merged = {**it, **extra}
        out.append(merged)
    return out


def slugify_unique(base_dir: Path, slug: str) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    candidate = base_dir / f"{slug}.md"
    n = 2
    while candidate.exists():
        candidate = base_dir / f"{slug}-{n}.md"
        n += 1
    return candidate


def write_articles(items: list[dict]) -> list[tuple[dict, Path]]:
    written = []
    for it in items:
        cat = it.get("category")
        if cat not in ("news", "educational"):
            continue
        article = it.get("wiki_article", "").strip()
        if not article:
            continue
        base = WIKI_NEWS if cat == "news" else WIKI_EDU
        path = slugify_unique(base, it["slug"])
        path.write_text(article + "\n", encoding="utf-8")
        written.append((it, path))
    return written


def update_index(category: str, new_entries: list[tuple[str, str, str]]):
    """new_entries: list of (slug, date, title) tuples."""
    if not new_entries:
        return
    base = WIKI_NEWS if category == "news" else WIKI_EDU
    index = base / "_index.md"
    text = index.read_text(encoding="utf-8")
    # remove placeholder if present
    text = re.sub(r"\n_Aun no hay articulos[^\n]*_\n?", "\n", text)
    # insert new lines right after the "## Articulos" header block
    lines_to_add = "\n".join(f"- [[{slug}]] — {date} — {title}" for slug, date, title in new_entries)
    if "## Articulos" in text:
        marker = "## Articulos"
        idx = text.find(marker)
        # move past the heading line
        newline = text.find("\n", idx)
        # skip any immediately-following blank lines or comments to get to first content line
        insert_at = newline + 1
        text = text[:insert_at] + "\n" + lines_to_add + "\n" + text[insert_at:]
    else:
        text += "\n\n## Articulos\n\n" + lines_to_add + "\n"
    index.write_text(text, encoding="utf-8")


def write_daily_dump(today: str, enriched: list[dict], errors: list[dict]):
    RAW_DAILY.mkdir(parents=True, exist_ok=True)
    path = RAW_DAILY / f"{today}.md"

    kept = [it for it in enriched if it.get("category") in ("news", "educational")]
    n_news = sum(1 for it in kept if it["category"] == "news")
    n_edu = sum(1 for it in kept if it["category"] == "educational")

    parts = [
        "---",
        f"date: {today}",
        f"items_found: {len(kept)}",
        f"items_news: {n_news}",
        f"items_educational: {n_edu}",
        f"fetch_errors: {len(errors)}",
        "---",
        "",
        f"# Daily Research — {today}",
        "",
    ]

    if errors:
        parts += ["## Errores de fetch", "", "| URL | Error |", "|-----|-------|"]
        for e in errors:
            parts.append(f"| {e['url']} | {e['error']} |")
        parts.append("")

    def render_section(title: str, cat: str, angle_label: str):
        parts.append(f"## {title}")
        parts.append("")
        section = [it for it in kept if it["category"] == cat]
        if not section:
            parts.append(f"_(sin items {cat} hoy)_")
            parts.append("")
            return
        for it in section:
            parts.append(f"### [{it.get('clean_title') or it['title']}]({it['url']})")
            parts.append(f"- **Fuente**: {it.get('source_name', '')}")
            parts.append(f"- **Fecha**: {it.get('published', '')}")
            for b in it.get("summary_bullets", []):
                parts.append(f"- {b}")
            parts.append(f"- **{angle_label}**: {it.get('business_angle', '')}")
            parts.append(f"- **Wiki**: `{ 'ai-news' if cat=='news' else 'ia-para-empresas' }/{it['slug']}`")
            parts.append("")

    render_section("News", "news", "Angulo para dueno de negocio")
    render_section("Educational", "educational", "Como implementarlo")

    parts.append("## Resumen para LinkedIn")
    parts.append("")
    top = kept[:3]
    if not top:
        parts.append("_(sin items hoy)_")
    else:
        for i, it in enumerate(top, 1):
            parts.append(f"{i}. **{it.get('clean_title') or it['title']}** — {it.get('business_angle', '')}")

    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"[{today}] Starting daily research")

    urls: list[tuple[str, str]] = []
    for fname in ("news-sources.md", "educational-sources.md"):
        urls.extend(load_source_urls(SOURCES_DIR / fname))

    seen_in_sources: set[str] = set()
    unique_sources = []
    for name, url in urls:
        if url in seen_in_sources:
            continue
        seen_in_sources.add(url)
        unique_sources.append((name, url))
    print(f"Loaded {len(unique_sources)} unique source URLs")

    all_items: list[dict] = []
    errors: list[dict] = []
    for name, url in unique_sources:
        print(f"  Fetching: {name} ({url})")
        items, err = fetch_feed(url)
        if err:
            errors.append({"url": url, "error": err})
            print(f"    ERROR: {err}")
            continue
        for it in items:
            it["source_name"] = name
            all_items.append(it)
        print(f"    got {len(items)} items")

    recent = [it for it in all_items if is_recent(it.get("published", ""), FETCH_WINDOW_HOURS)]
    print(f"{len(recent)} items within {FETCH_WINDOW_HOURS}h window (of {len(all_items)} total)")

    seen_urls = load_seen_urls(DEDUP_LOOKBACK_DAYS)
    new_items = [it for it in recent if it["url"] not in seen_urls]
    print(f"{len(new_items)} items after dedup ({len(recent) - len(new_items)} seen before)")

    new_items = new_items[:MAX_ITEMS_PER_DAY]
    print(f"Processing up to {len(new_items)} items with Claude")

    enriched: list[dict] = []
    if new_items:
        try:
            enriched = classify_and_compile(new_items)
        except Exception as e:
            errors.append({"url": "(classify_and_compile)", "error": str(e)})
            print(f"ERROR during Claude call: {e}")

    written = write_articles(enriched)
    print(f"Wrote {len(written)} wiki articles")

    new_by_cat: dict[str, list[tuple[str, str, str]]] = {"news": [], "educational": []}
    for it, path in written:
        new_by_cat[it["category"]].append((path.stem, today, it.get("clean_title") or it["title"]))

    for cat, entries in new_by_cat.items():
        update_index(cat, entries)

    write_daily_dump(today, enriched, errors)
    print(f"Daily dump written: {RAW_DAILY / (today + '.md')}")
    print(f"Done. news={len(new_by_cat['news'])} educational={len(new_by_cat['educational'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
