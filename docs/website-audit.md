# WeianData Website Audit

**Status:** Draft for review before preview deployment
**Date:** 2026-07-10
**Scope:** Complete static bilingual website in `weiandata/website`
**Auditor note:** This document reports findings only. No production files were
modified. The audit does not redesign the website; every recommendation is
scoped to preserve the existing static architecture per the
[Website Migration Guide](WeianData_Website_Repository_Migration_Guide.md).

---

## 1. What was reviewed

| Area | Coverage |
| --- | --- |
| Chinese HTML pages | `index.html`, `tools.html`, `methods.html`, `learn.html`, `article.html` |
| English HTML pages | `en/index.html`, `en/tools.html`, `en/methods.html`, `en/learn.html`, `en/article.html` |
| Shared runtime | `support.js` (dc-runtime: React-based client renderer) |
| Article loading logic | `article.html` + `en/article.html` `loadArticle()` / `render()` |
| Article libraries | `articles/` (80: A01–A30, M01–M50) and `articles-en/` (80) |
| SEO / discovery | `robots.txt`, `sitemap.xml`, `llms.txt`, canonical tags |
| External dependencies | React, ReactDOM, Babel, KaTeX, Google Fonts (Noto Sans SC) |
| Positioning reference | `llms.txt`, `README.md`, migration guide (see §2 caveat) |
| Validation | `scripts/validate_site.py` (re-run: **passes** — 10 pages, 160 articles) |

**Structural integrity (positive).** The migration itself is clean. Relative
paths were verified page-by-page and are correct in both directions
(`en/` pages use `../support.js`, `../articles-en/…`, `../index.html`; root
pages use `./support.js`, `articles/…`). No broken internal links, no obsolete
`.dc.html` references, and no `localhost` / `127.0.0.1` / `file://` /
absolute-path leaks were found. CN/EN article identifiers are aligned (80/80,
identical filenames). The findings below concern rendering strategy, SEO,
content leakage, unsupported claims, and mainland-China reliability — not the
file-structure refactor, which is sound.

## 2. Caveat on the business-plan comparison

The task references a **WeianData business plan** and **Engineering Handbook**.
Neither is present in this repository (the handbook lives in the external
`weiandata/.github` repo; no business-plan document exists in-tree). To avoid
unsupported assumptions, positioning was compared against the in-repo
positioning artifacts that encode it: `llms.txt` (the explicit positioning
statement), `README.md`, and the migration guide. Where a claim could not be
verified against repository evidence, it is flagged rather than assumed true
(see High-3, High-5).

---

## 3. Findings by severity

Severity legend: **Critical** = blocks or defeats the purpose of a preview/
production launch; **High** = launch-blocking for the mainland-China audience or
materially damaging; **Medium** = should fix before or shortly after launch;
**Low** = polish / follow-up.

### CRITICAL

#### C1 — The entire site is client-rendered and hard-depends on unpkg.com; in mainland China it can render as a blank page

- **Affected files:** `support.js` (lines ~1594–1687), all 10 HTML pages, `en/*`
- **Issue:** Every page's real content lives inside a `<x-dc>` block that
  `support.js` immediately hides (`x-dc{display:none!important}`) and then
  re-renders with React. `support.js` loads React and ReactDOM from
  `https://unpkg.com/...` and only boots after both resolve
  (`loadReactUmd().then(init)`). unpkg.com is frequently slow or unreachable from
  mainland China. If either script is blocked, `getReact()` throws, `init()`
  never runs, and the page shows **nothing** — the raw markup stays
  `display:none`.
- **Impact:** For the stated target audience (mainland Chinese research
  institutes, 科协 system, universities, government-adjacent survey sponsors),
  the site may be entirely blank — no content, no navigation, no contact email.
  This defeats the whole purpose of the site and directly contradicts the
  "trustworthy / reliable delivery" positioning.
- **Recommended action:** Localize React + ReactDOM to `assets/vendor/` and load
  them from the same origin (the migration guide already scopes this as
  `refactor/localize-third-party-assets`). As a defense-in-depth measure,
  provide a `<noscript>` / no-render fallback (at minimum a visible company name,
  summary, and `contact@weiandata.com`) so a boot failure never yields a blank
  page. Do this **before** any mainland-facing preview.

#### C2 — No server-rendered content and no `<title>`/`<meta description>` on any page → the site is effectively invisible to search engines and AI crawlers

- **Affected files:** all 10 HTML pages, `sitemap.xml`, `robots.txt`
- **Issue:** Grep across all HTML confirms **zero `<title>` tags and zero
  `<meta name="description">`**. Titles are set only at runtime, after React
  boots, via `document.title = …`. All human-readable content is inside the
  hidden `<x-dc>` block and only appears after client-side rendering. A crawler
  that does not execute JS (or that fails to load React from unpkg) receives a
  page with no title, no description, and no body content.
- **Impact:** Major SEO defect. `robots.txt` deliberately invites Baiduspider,
  GPTBot, ClaudeBot, PerplexityBot, Bytespider, etc., and `sitemap.xml`/`llms.txt`
  exist specifically to be discovered — but the pages those crawlers fetch are
  empty shells. The 160-article content library (a core marketing asset) is not
  indexable. This undermines the lead-generation intent of the site.
- **Recommended action:** At minimum, add a static `<title>` and
  `<meta name="description">` to the `<head>` of every page (these live outside
  `<x-dc>` and are safe to hardcode without touching the rendered design).
  Strategically, evaluate pre-rendering the static HTML (a static snapshot of the
  rendered DOM, or a small build step / SSG) so crawlers and no-JS clients get
  real content — this is the highest-leverage SEO fix and pairs with C1.

#### C3 — Internal editorial / go-to-market notes leak to visitors on Chinese long-form article pages (A05–A30)

- **Affected files:** `article.html` (`render()`, the strip block ~lines 223–231);
  `articles/A05.md`–`articles/A30.md`
- **Issue:** Each article markdown opens with a `>` blockquote that is an
  **internal production note** (content channel plan, business line, selling
  points). `article.html` only removes this blockquote when it matches a narrow
  keyword set: `/手册|一鱼四吃|投放|内部|曝光红线/`. Notes lacking those exact
  words are rendered to users. Confirmed examples now publicly visible:
  - A05: *"配套 Q02 的深度版。适合公众号转载与 B站图解视频。"*
  - A18: *"技术旗舰文。IRTC 差异化能力的深度阐述，适合投稿统计之都（cosx.org）改写版。"*
  - A21: *"测评实务线。面向项目管理者的体系化长文，商务价值高。"*
  - A27: *"配套 Q26 的深度版。商务转化线，以「帮甲方避坑」立场建立信任。"*
  - …and every A05–A30 article (26 pages) whose note lacks the keywords.
  (A01–A04 happen to contain a keyword and are stripped; M-article blockquotes
  are reader-facing intros and are intentionally kept.)
- **Impact:** Visitors and crawlers see internal marketing strategy, channel
  plans, and "selling point" annotations on public article pages. This looks
  unprofessional, exposes go-to-market internals, and erodes the credibility the
  site is trying to build. The English reader also sees the identical notes in
  the committed `articles-en/*` sources (translated), though `en/article.html`
  strips them at render (see M1).
- **Recommended action:** Do not rely on a keyword allowlist. Either (a) strip
  **any** leading blockquote that immediately follows the H1 in article
  rendering (matching the English page's behavior), or (b) move internal notes
  out of the published markdown entirely (e.g., an HTML comment or a separate
  editorial file). Option (a) is the smallest, safest change and fixes C3 and M1
  together. Re-scan all 160 files afterward.

### HIGH

#### H1 — ICP filing is a placeholder; the site cannot legally serve from the intended mainland (Tencent Cloud) host

- **Affected files:** footers of all Chinese pages (`© 2026 京ICP备 000000 号（待备案）`);
  `en/index.html` (`© 2026 · ICP filing pending`)
- **Issue:** The ICP number is a `000000` placeholder marked "待备案" (filing
  pending). A mainland Tencent Cloud lightweight server (the stated deployment
  target per README/migration guide) will not serve an un-filed domain, and doing
  so is non-compliant.
- **Impact:** Hard blocker for mainland production. A preview on non-mainland
  infrastructure can proceed, but production on the stated host cannot until the
  real ICP (and 公安备案) is issued and inserted. Already tracked as Priority 1 in
  the migration guide; restated here because it gates the deployment this audit
  precedes.
- **Recommended action:** Complete ICP filing; replace the placeholder in all
  footers with the real number; add the 公安网备 record. Keep CN/EN wording
  consistent (see M7).

#### H2 — Additional mainland-blocked CDNs: KaTeX (jsDelivr) and Noto Sans SC (Google Fonts)

- **Affected files:** `article.html` / `en/article.html` (KaTeX CSS+JS from
  `cdn.jsdelivr.net`); all 10 pages (`fonts.googleapis.com`)
- **Issue:** Article equations depend on KaTeX from jsDelivr; every page requests
  the Noto Sans SC webfont from Google Fonts. Both hosts are unreliable/blocked in
  mainland China. Google Fonts degrades gracefully (system-font fallback in the
  `body` stack), but KaTeX failure leaves equations as raw TeX source.
- **Impact:** On article pages that use math, mainland readers may see unrendered
  `$…$`/`$$…$$` fragments; fonts fall back (acceptable but off-brand).
- **Recommended action:** Localize KaTeX (CSS, JS, and required font files) and
  the Noto Sans SC subset into `assets/vendor/` and `assets/fonts/`, in the same
  follow-up change as C1. `docs/external-dependencies.md` already recommends
  this; execute it before the mainland preview.

#### H3 — `llms.txt` names specific national surveys as served work, which is unverified and contradicts the site's own confidentiality disclaimers

- **Affected files:** `llms.txt` ("差异化" section) vs `tools.html` / `en/index.html`
- **Issue:** `llms.txt` states the company serves *"国家级调查（公民科学素质调查、
  中小学学生科学素养调查、公民数字素养调查同类项目）"*. The rendered site
  repeatedly asserts the opposite discipline: `tools.html` — *"案例不含任何客户项目
  名称与敏感数据"*; article A26's note — *"不涉及任何具体项目与客户"*. Naming named
  national programs (even softened with "同类") in a machine-readable file that AI
  search engines ingest is an unsupported claim with no corroborating evidence in
  the repository, and it undercuts the "we never expose client work" positioning
  that is central to the brand.
- **Impact:** Reputational and potentially contractual risk; AI assistants may
  surface WeianData as having worked on named government surveys. Inconsistent
  messaging between the public site and the LLM-discovery file.
- **Recommended action:** Reword `llms.txt` to describe capability/domain without
  naming specific national programs (e.g., "大型公共素养与教育质量调查类项目的
  方法学能力"), aligning it with the on-site "no client project names" stance.
  Confirm any client reference is contractually clearable before publishing.

#### H4 — The 160 articles are not individually indexable (single static canonical, no per-article sitemap entries, no static titles)

- **Affected files:** `article.html` / `en/article.html` (`<link rel="canonical"
  href=".../article.html">`), `sitemap.xml`
- **Issue:** All 80 Chinese and 80 English articles are served from the same URL
  with a `?id=` query parameter, but every article variant declares the **same**
  static canonical (`/article.html`, `/en/article.html`) and the `?id=` routes are
  **absent from `sitemap.xml`**. Combined with C2 (no static title/body), search
  engines see one titleless page per language, not 160 distinct articles.
- **Impact:** The content library — explicitly built as a discovery/marketing
  asset (`learn.html`: "全部 80 篇均可在本站阅读"; `robots.txt` invites AI crawlers)
  — contributes almost nothing to organic discovery. Direct contradiction between
  the content investment and its findability.
- **Recommended action:** Decide the article URL strategy (either per-article
  routes/prerendered pages, or accept query-param canonicals but make them
  self-referencing and list them in the sitemap). Pairs with C2; at minimum emit
  a per-article canonical that includes the `id` and add representative article
  URLs to `sitemap.xml`.

#### H5 — Capability claim "已在百万级样本上验证" overstates what the tools page substantiates

- **Affected files:** `methods.html` (§1: IRTC "已在百万级样本上验证");
  `index.html` STATS ("10⁶ · 样本级 IRT 全流程") vs `tools.html` (IRTC results:
  *"流式引擎已在原型基准中完成百万样本、多维 GPCM 估计"*)
- **Issue:** The detailed case study is carefully hedged — "原型基准" (prototype
  benchmark). The homepage stat and the methods page restate this as a headline
  capability ("已在百万级样本上验证" / "样本级 IRT 全流程"), dropping the
  "prototype benchmark" qualifier. The stronger phrasing is not supported by any
  further evidence in the repository, and IRTC itself is marked "CRAN 即将发布"
  (not yet released).
- **Impact:** Unsupported / inconsistent product claim across pages; a
  knowledgeable prospect who reads all three pages will notice the walk-back,
  which damages the credibility the brand depends on.
- **Recommended action:** Make the three pages consistent with the most defensible
  statement (the tools-page "prototype benchmark" framing), e.g. homepage/methods
  should say the engine has completed million-scale estimation "在原型基准中" /
  "in prototype benchmarks" rather than "已验证". Only upgrade the wording when
  independent, citable evidence exists.

### MEDIUM

#### M1 — CN and EN article readers strip the leading blockquote differently, causing inconsistent bilingual content

- **Affected files:** `article.html` vs `en/article.html` (`render()`)
- **Issue:** `en/article.html` **always** strips the leading blockquote (comment:
  "always strip the leading blockquote"), while `article.html` strips only on a
  keyword match. Consequences: (a) English A-article internal notes are correctly
  hidden but Chinese ones leak (C3); (b) English **M-articles lose the
  reader-facing intro teaser** (e.g., M01's "本专题第一篇…") that Chinese readers
  see, so the two languages present different content for the same article.
- **Impact:** Bilingual inconsistency; English readers get a slightly poorer
  reading experience (missing intros) while Chinese readers get leaked notes.
- **Recommended action:** Unify the two renderers on one rule. Recommended:
  strip any leading blockquote in both languages **and** move reader-facing M
  intros into the article body (or a dedicated intro field) so both languages
  keep them. Resolves C3 and M1 coherently.

#### M2 — No `<html lang>` attribute on any page

- **Affected files:** all 10 HTML pages (`<html>` with no `lang`)
- **Issue:** Neither the Chinese nor English pages declare a language.
- **Impact:** Screen readers may mis-pronounce content; hurts accessibility and
  bilingual SEO signals; browsers cannot pick correct hyphenation/typography.
- **Recommended action:** Add `lang="zh-CN"` to root pages and `lang="en"` to
  `en/*` pages. One-line, no design impact.

#### M3 — No `hreflang` alternate links between Chinese and English equivalents

- **Affected files:** all 10 HTML pages
- **Issue:** Language switching is nav-only; there are no
  `<link rel="alternate" hreflang="…">` tags pairing each page with its
  translation.
- **Impact:** Search engines cannot associate the CN/EN versions, weakening
  bilingual indexing and risking duplicate-language dilution.
- **Recommended action:** Add reciprocal `hreflang` (`zh-CN`, `en`, `x-default`)
  link tags in each page `<head>` (outside `<x-dc>`, safe to hardcode).

#### M4 — Accessibility gaps: focus states, form labels, and color contrast

- **Affected files:** all 10 HTML pages; `learn.html` / `en/learn.html` search input
- **Issue:** (a) Interactive hover styling is applied via a custom `style-hover`
  attribute (handled by the runtime) with **no `:focus`/`:focus-visible`**
  equivalent, so keyboard users get no visible focus feedback. (b) The learn-page
  search `<input data-searchbox>` has a placeholder but **no associated
  `<label>`**. (c) Muted text color `#8A857A` on the `#FAF8F2`/`#F3F0E6`
  backgrounds is used pervasively for small monospace labels and likely fails
  WCAG 2.1 AA contrast (≈2.9:1 vs the 4.5:1 requirement).
- **Impact:** Keyboard and low-vision users are disadvantaged; fails common
  accessibility acceptance criteria.
- **Recommended action:** Add visible `:focus-visible` outlines for links/buttons;
  add a visually-hidden `<label>` (or `aria-label`) to the search input; darken
  `#8A857A` to meet AA where it carries meaningful text. Verify with an automated
  contrast checker.

#### M5 — Canvas visualizations lack text alternatives

- **Affected files:** `index.html` / `en/index.html` (hero `data-flow`, `data-spark`)
- **Issue:** The particle-flow and sparkline `<canvas>` elements have no
  `role`/`aria-label` or adjacent text alternative. They are largely decorative,
  but the animated `n = …` counter conveys a "million-scale" impression with no
  accessible equivalent.
- **Impact:** Minor accessibility gap; screen-reader users miss the visual
  narrative.
- **Recommended action:** Mark decorative canvases `aria-hidden="true"`; if the
  counter is meaningful, expose an accessible text summary. Low effort.

#### M6 — Footer copyright / ICP wording differs between Chinese and English

- **Affected files:** CN footers (`惟安数据科技（北京）有限公司 · … 京ICP备 000000
  号（待备案）`) vs `en/index.html` (`WEIAN Data Technology (Beijing) Co., Ltd. ·
  … ICP filing pending`)
- **Issue:** The two languages present the legal entity and filing status in
  different formats.
- **Impact:** Minor bilingual inconsistency; both must carry the real ICP once
  filed (H1).
- **Recommended action:** Standardize footer legal text across languages when the
  ICP number is inserted.

### LOW

#### L1 — `docs/external-dependencies.md` lists Babel Standalone as a loaded runtime dependency, but it is never actually loaded

- **Affected files:** `docs/external-dependencies.md`; `support.js` (`ensureBabel`)
- **Issue:** Babel (`unpkg.com/@babel/standalone`) is only fetched when a page
  uses a JSX `x-import`. No page does, so Babel is never requested at runtime. The
  dependency doc presents it as an active dependency.
- **Impact:** Documentation slightly overstates the runtime dependency surface.
- **Recommended action:** Note in the dependency doc that Babel is only loaded on
  demand for JSX imports and is currently unused; still localize it if/when JSX is
  introduced.

#### L2 — No favicon, touch icon, or web manifest

- **Affected files:** all 10 HTML pages
- **Issue:** No `<link rel="icon">`; browser tabs show a blank/default icon.
- **Impact:** Minor polish/branding gap. Already in the migration guide Priority 2
  follow-ups.
- **Recommended action:** Add a favicon (and optionally an SVG/PNG touch icon)
  referenced from each `<head>`.

#### L3 — No custom 404 page

- **Affected files:** repository root (none present); `docs/deployment.md` expects
  Nginx to "return real 404 responses"
- **Issue:** There is no branded error page for missing routes/articles.
- **Impact:** Minor UX gap on bad URLs (e.g., `article.html?id=A99` shows an
  inline JS failure message, which is handled, but hard 404s hit the bare server
  page).
- **Recommended action:** Add a simple static `404.html` and wire it in the Nginx
  config during deployment.

#### L4 — Large per-page inline runtime logic is duplicated across pages

- **Affected files:** `index.html`, `en/index.html`, and others (repeated
  `setupCtaFeedback`/reveal/IntersectionObserver blocks)
- **Issue:** Each page inlines near-identical animation/logic classes.
- **Impact:** Maintainability only (no user-facing defect); a fix in one page must
  be replicated.
- **Recommended action:** Optional future consolidation into shared logic; out of
  scope for the migration and not required before launch.

---

## 4. Summary counts

| Severity | Count | IDs |
| --- | --- | --- |
| Critical | 3 | C1 (CDN/blank-page), C2 (JS-only render / no SEO metadata), C3 (internal-note leak) |
| High | 5 | H1 (ICP placeholder), H2 (KaTeX/Fonts CDN), H3 (llms.txt claims), H4 (article indexability), H5 (overstated claim) |
| Medium | 6 | M1 (CN/EN strip mismatch), M2 (`lang`), M3 (hreflang), M4 (a11y), M5 (canvas alt), M6 (footer text) |
| Low | 4 | L1 (Babel doc), L2 (favicon), L3 (404), L4 (duplicated JS) |

**Unsupported / unverifiable claims identified:** H3 (named national surveys in
`llms.txt`), H5 ("已在百万级样本上验证" vs "原型基准"). Absolute claims that are
consistent with stated process and not flagged as defects but worth keeping
truthful: "100% 敏感数据不出客户内网", "50+ 组自动化测试" (26+13+16 = 55 across the
three packages — supported), "3 个自研 R 包 · 含 CRAN 发布" (only `ratecalib` is
actually on CRAN; IRTC and mergecalib are "即将发布" — wording is defensible as
written but keep it accurate as status changes).

**Bilingual inconsistencies identified:** C3/M1 (article blockquote handling),
M6 (footer legal text). Navigation, service descriptions, tool cards, methods
sections, and article inventories are otherwise faithfully mirrored between
languages.

**Missing pages:** None broken. All five routes exist in both languages and the
sitemap. The "missing" gaps are non-page assets: favicon (L2), 404 page (L3),
and static SEO metadata/pre-rendered content (C2/H4).

---

## 5. Prioritized implementation plan

Ordered by launch-gating priority. Items marked **[before mainland preview]**
should be done before any preview aimed at the mainland-China audience; the rest
can follow in normal PR cadence. Keep the static architecture; do not introduce
a framework build unless C2's pre-rendering option is explicitly approved.

### Phase 0 — Launch blockers (before mainland preview)

1. **Localize CDN dependencies** (C1, H2). Move React, ReactDOM, KaTeX (+ fonts),
   and Noto Sans SC into `assets/vendor/` and `assets/fonts/`; point all pages at
   same-origin copies. Add a `<noscript>`/no-render fallback with company name,
   one-line summary, and `contact@weiandata.com`. *(Branch:
   `refactor/localize-third-party-assets`, already scoped in the migration guide.)*
2. **Stop the internal-note leak** (C3, M1). Change `article.html` to strip any
   leading blockquote following the H1 (match `en/article.html`), and/or remove
   internal notes from published markdown. Re-scan all 160 files. Decide where
   reader-facing M-intros should live so both languages keep them.
3. **Add static `<title>` + `<meta name="description">`** to every page `<head>`
   (C2). Smallest fix that restores basic crawlability and social/share previews.
4. **Resolve ICP** (H1). Complete filing; replace `000000（待备案）` and
   `ICP filing pending` with the real number and 公安备案; unify CN/EN wording (M6).

### Phase 1 — SEO and content correctness

1. **Article indexability** (H4, C2). Choose the article URL/canonical strategy;
   emit `id`-aware canonicals and add representative article URLs to
   `sitemap.xml`. Evaluate a pre-rendered static snapshot so crawlers and no-JS
   clients get real content (the durable fix for C2).
2. **Fix unsupported/inconsistent claims** (H3, H5). Reword `llms.txt` to drop
   named national surveys; align homepage/methods "million-scale" wording with the
   tools page's "prototype benchmark" framing.
3. **Add `<html lang>` and reciprocal `hreflang`** tags (M2, M3).

### Phase 2 — Accessibility and polish

1. **Accessibility pass** (M4, M5): visible `:focus-visible` states, a label for
   the search input, AA-compliant contrast for muted text, `aria-hidden` on
   decorative canvases.
2. **Favicon + 404 page** (L2, L3); Nginx wiring for the 404 at deploy time.
3. **Documentation truth-up** (L1): correct the Babel entry in
   `docs/external-dependencies.md`. Optional: consolidate duplicated inline JS
   (L4) in a later maintenance pass.

### Validation gate

Before the preview is promoted:

- Re-run `python3 scripts/validate_site.py` (structural — currently passes).
- Manually verify, over a local HTTP server **with unpkg/jsDelivr/Google Fonts
  blocked** (to simulate mainland conditions), that every page still renders,
  navigation and language switching work, articles load, and no internal notes
  appear. The current `validate_site.py` does **not** catch C1–C3, H2–H5, or the
  accessibility items, so this manual gate is required in addition to CI.

---

*Prepared as a pre-deployment audit. Findings are evidence-based against the
repository state at commit time; no production files were changed except the
creation of this document.*
