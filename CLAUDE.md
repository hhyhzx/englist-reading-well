# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-page PWA for English intensive reading vocabulary study, targeting Chinese middle school exam (中考) preparation. All code lives in a single `index.html` — no framework, no build step, no package manager.

## Commands

```bash
# Start the dev server (auto-opens browser)
python start_app.py
```

The server runs on `0.0.0.0:8080` with `Cache-Control: no-cache` headers. Access from phone on same LAN via the printed IP.

No lint, test, or build commands exist.

## Architecture

**Single-file app.** `index.html` contains all HTML, CSS (`<style>`), and JS (`<script>`). The CSS/JS is minified but not obfuscated. When editing, keep styles and scripts inline.

**PWA setup:**
- `manifest.json` — PWA manifest with standalone display, portrait orientation, inline SVG icon
- `sw.js` — service worker that always fetches fresh (never caches); clears any old caches on activate

**Data model — `DAYS[]` array (18 entries, indices 0–17):**
Each day entry has:
- `title` — article title (Chinese)
- `core` — 核心词汇: `[word, IPA, part-of-speech, Chinese meaning]`
- `advanced` — 提高词汇 (same structure)
- `recognition` — 识记词汇 (same structure)
- `phrases` — `[English phrase, Chinese meaning]`
- `patterns` — 句型: `[formula name, example sentence (with `<kw>`/`<ph>` markup), structure breakdown, exam tip]`

Vocabulary items across all three lists are concatenated in this order in `getItems()`: core → advanced → recognition.

Note: two entries share the title "飞行员火车着陆" (indices 2 and 3) — they are different articles with different vocabulary sets. This is a known data issue, not a bug in the rendering logic.

**Known bugs:**
- `listenedCount()` builds an `all` array from all item types but never uses it — dead code. The counting loop instead iterates `listened` keys, which means it only counts items that have been explicitly marked listened (not total items).
- `listenedCount()` counts listened items across **all modes** for the current day (not just the currently active mode), since its loop matches any `listen_v1` key starting with `currentDay`.

**Modes (tabs within each day):**
- `vocab` — flashcard with word/IPA/speaker on front, Chinese meaning on tap. `getCategory(idx)` splits items into core/advanced/recognition tiers based on their position in the concatenated list and renders a colored tag (`tag-core` red, `tag-adv` blue, `tag-rec` green).
- `phrase` — phrase flashcard with `tag-phr` orange badge
- `pattern` — sentence structure card showing formula, parsed example (with `<kw>`/`<ph>` markup rendered as colored spans), and exam note

**State:** `currentDay` (0–17 for 18 days), `currentMode` (`'vocab'|'phrase'|'pattern'`), `currentIdx` (position within current mode's items). Card flip state stored on `window._flipped` (reset to `false` on every `render()`).

**Listening tracking:** `markListened()` is called by `speak()` (not on card flip). It writes `day_mode_index → 1` into `localStorage` under key `listen_v1`. A ✅ checkmark is shown next to the speaker icon for listened items. The header shows `(listenedCount/totalCount)` progress for the current day.

**Navigation:** keyboard arrows (left/right), swipe left/right on touch, on-screen prev/next buttons. Spacebar flips the card.

**Speech:** uses `window.speechSynthesis` with `en-US` lang, rate 0.85. For pattern mode, the example sentence is stripped of `<kw>`/`<ph>` HTML tags before being passed to `speak()`.

**Day tabs with pagination:** Day tabs are dynamically generated from `DAYS[]` via `renderTabs()`. Badges use the first 4 characters of each day's `title`. Tabs are paginated — `PER_PAGE = 7` tabs shown at a time with `◀`/`▶` navigation buttons. `currentPage` tracks the visible page. A sort toggle (`sortOrder`) switches between ascending (1→18) and descending (18→1) order. `getDayIndex(di)` and `getDisplayIndex(ai)` map between display position and actual DAYS array index.

**Content density:** Days 1–7 are the original set with richer vocabulary (30–50 core items, 6–12 advanced, 2–3 recognition) and 5–7 sentence patterns per day. Days 8–18 were added later and are leaner: ~20–25 core items, ~4–6 advanced, 0–1 recognition, and exactly 4 patterns each. Some later days (e.g., Days 16–18) have empty `recognition` arrays.

**`.nojekyll`** at the repo root is for GitHub Pages deployment — the site is served as a static PWA.

## Git-ignored files

Images (`*.jpg`, `*.png`), docx files, and Python files except `start_app.py` are gitignored. The `test*.js` files in the root are untracked alternate versions of the inline script — they are not part of the app.
