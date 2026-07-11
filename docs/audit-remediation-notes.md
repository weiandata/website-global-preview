# Website Audit — Remediation Notes

**Status:** Living record; updated as remediation progresses
**Date:** 2026-07-10
**Source of findings:** [website-audit.md](website-audit.md)
**Owner:** WeianData

This document records the disposition of every finding in the website audit: what
was fixed in code (with the pull request that landed it) and what is intentionally
**not** a code change under the remediation guardrails — with the reason and a
recommended action. It exists so that, before preview deployment, every audit
finding has a traceable decision rather than a silent omission.

Guardrails that shaped these decisions: preserve the current architecture and
visual design; no framework migration; no rewriting marketing copy without
evidence; do not invent products, customers, publications, or partnerships; do
not implement business decisions or infrastructure changes as code — document
them instead.

---

## 1. Disposition summary

| ID | Severity | Finding | Disposition | Reference |
| --- | --- | --- | --- | --- |
| C3 | Critical | Internal editorial notes leaked on Chinese article pages | Fixed | PR #5 |
| M1 | Medium | CN/EN article renderer inconsistency | Fixed | PR #5 |
| C2 | Critical | No static `<title>`/`<meta description>` | Fixed (metadata) | PR #6 |
| C2 | Critical | Body content only client-rendered (crawlers get a shell) | Recommended | §3.5 |
| M2 | Medium | No `<html lang>` | Fixed | PR #7 |
| M3 | Medium | No `hreflang` alternates | Fixed | PR #7 |
| M4 | Medium | No keyboard focus indicator; unlabeled search input | Fixed | PR #8 |
| M4 | Medium | Low-contrast muted text | Recommended | §3.6 |
| M5 | Medium | Decorative canvases lack text alternative | Fixed | PR #8 |
| L3 | Low | No 404 page | Fixed | PR #9 |
| L2 | Low | No favicon | Fixed | PR #10 |
| H4 | High | Articles not individually indexable (canonical) | Fixed (canonical) | PR #11 |
| H4 | High | Article URLs absent from `sitemap.xml` | Recommended | §3.7 |
| L1 | Low | `external-dependencies.md` overstated Babel | Fixed | PR #12 |
| C1 | Critical | CDN React/ReactDOM → blank page in mainland China | Fixed | PR #13 |
| H2 | High | KaTeX loaded from jsDelivr | Fixed | PR #13 |
| H2 | High | Noto Sans SC loaded from Google Fonts | Recommended | §3.8 |
| H1 | High | ICP filing is a placeholder | Recommended | §3.1 |
| H3 | High | `llms.txt` names specific national surveys | Recommended | §3.2 |
| H5 | High | "million-scale verified" overstates the tools page | Recommended | §3.3 |
| M6 | Medium | CN/EN footer legal text differs | Recommended | §3.4 |
| L4 | Low | Duplicated inline page JS | Recommended | §3.9 |

Where a finding is split across rows (C2, M4, H4, H2), the code-addressable half
was implemented and the remaining half is recommended below.

---

## 2. Implemented (merged to `main`)

Nine pull requests, each a single logical group, all additive and CI-green:

| PR | Title | Findings |
| --- | --- | --- |
| #5 | fix: prevent editorial note leakage in article renderer | C3, M1 |
| #6 | feat: add static page titles and meta descriptions | C2 (metadata) |
| #7 | feat: add html lang attributes and hreflang alternates | M2, M3 |
| #8 | feat: add keyboard focus, input label, and decorative-canvas a11y | M4 (focus/label), M5 |
| #9 | feat: add static bilingual 404 error page | L3 |
| #10 | feat: add site favicon | L2 |
| #11 | feat: set id-aware canonical and hreflang on article pages | H4 (canonical) |
| #12 | docs: correct Babel dependency status in external-dependencies | L1 |
| #13 | feat: localize React, ReactDOM and KaTeX | C1, H2 (KaTeX) |

None of these changed page layout, typography, color, spacing, animation,
navigation, or existing URLs. React, ReactDOM, and KaTeX are now served
same-origin, removing the primary mainland-China blank-page risk (verified in a
real browser: local assets load `200`, zero CDN calls, no console errors).

---

## 3. Recommended (not implemented as code — with rationale)

Each item below was deliberately left out of the code remediation. For each: why
it is not a source-code change under the guardrails, and the recommended action.

### 3.1 H1 — Complete ICP filing (deployment / legal)

- **Why not code:** the ICP/公安 record is a regulatory filing, not a repository
  change. The footers carry a `京ICP备 000000 号（待备案）` placeholder.
- **Impact:** a mainland Tencent Cloud host will not legally serve the domain
  until a real ICP is issued; this blocks production, though not an off-mainland
  preview.
- **Recommended action:** complete the ICP (and 公安网备) filing; then a small
  code change replaces the placeholder in all footers with the real number, in a
  single PR — coordinate with M6 so CN/EN wording lands together.

### 3.2 H3 — Rewrite `llms.txt` national-survey claims (business)

- **Why not code:** the file names specific national programs (公民科学素质调查,
  中小学学生科学素养调查, 公民数字素养调查) as served work. Changing or keeping
  such a claim is a business/legal decision, and the wording must be owner-approved
  — outside "no unsupported claims / no invented customers".
- **Impact:** unverifiable claim that also contradicts the site's own
  confidentiality stance ("案例不含任何客户项目名称与敏感数据"). AI assistants may
  surface WeianData as having worked on named government surveys.
- **Recommended action:** reword to describe capability/domain without naming
  specific programs (e.g. "大型公共素养与教育质量调查类项目的方法学能力"), once the
  owner confirms what is contractually clearable. Then a one-file docs change.

### 3.3 H5 — Reconcile "million-scale" capability wording (product)

- **Why not code:** the homepage/methods "已在百万级样本上验证" vs the tools page's
  hedged "原型基准中完成百万样本" is a product-claim decision; the guardrails forbid
  rewriting marketing copy without evidence or owner sign-off.
- **Impact:** an inconsistent, arguably overstated claim across pages undermines
  credibility for a technically literate audience.
- **Recommended action:** owner picks the defensible phrasing (recommended: the
  tools-page "prototype benchmark" framing) and applies it to the homepage stat
  and methods §1. Upgrade only when independent, citable evidence exists.

### 3.4 M6 — Standardize CN/EN footer legal text (business)

- **Why not code now:** the two languages present the entity and filing status
  differently (`京ICP备 000000 号（待备案）` vs `ICP filing pending`). The final
  text depends on the real ICP number (H1), so it should land with that filing.
- **Recommended action:** when H1 completes, standardize footer legal text across
  both languages in the same PR.

### 3.5 C2 (remaining) — Pre-render body content (architectural)

- **Why not code now:** all content is rendered client-side inside `<x-dc>`. A
  crawler that does not execute JS still receives an empty body. The static
  `<title>`/`<meta>` (PR #6) restores basic crawlability, but full content
  discoverability needs a pre-rendered static snapshot or a small build step —
  an architectural change the guardrails reserve for a separately reviewed effort
  ("no framework migration unless explicitly approved").
- **Recommended action:** evaluate a build-time static snapshot of the rendered
  DOM (or a static-site-generator adoption) as a dedicated, separately reviewed
  project. This is the durable fix and also unblocks §3.7.

### 3.6 M4 (remaining) — Raise muted-text contrast (design)

- **Why not code:** the muted `#8A857A` on the cream/`#F3F0E6` backgrounds likely
  fails WCAG AA for small text, but darkening it changes palette values, and the
  design is "already visually approved" (preserve colors).
- **Recommended action:** design-owner approves a darker muted token that meets
  AA (~4.5:1) for text-bearing uses; then apply as a token change. Keyboard focus
  and the form label (the additive half of M4) are already fixed in PR #8.

### 3.7 H4 (remaining) — List article URLs in `sitemap.xml`

- **Why not code now:** two blockers. (a) `scripts/validate_site.py` requires the
  sitemap to equal exactly the ten page canonicals; adding article URLs would fail
  CI unless the validator contract is changed too. (b) Until body pre-rendering
  (§3.5) lands, those URLs return an empty shell to crawlers, so listing them adds
  little value. The id-aware canonical/hreflang half is already fixed in PR #11.
- **Recommended action:** sequence after §3.5; then add representative (or all)
  article routes to `sitemap.xml` and update the validator's expected-URL set in
  the same PR.

### 3.8 H2 (remaining) — Self-host Noto Sans SC (font subsetting)

- **Why not code now:** React/ReactDOM/KaTeX are already localized (PR #13). A
  full CJK webfont is large and Google serves it as many dynamically
  unicode-range-split subsets; naive vendoring is impractical and risky in one
  change, and the font already degrades gracefully to the system CJK stack
  (`PingFang SC`, `Microsoft YaHei`).
- **Recommended action:** generate a subsetted Noto Sans SC (weights 400/500/700/900)
  limited to the glyphs the site uses, place it under `assets/fonts/` with an
  `@font-face` + local stylesheet, and drop the Google Fonts link — as its own PR
  with a rendering check.

### 3.9 L4 — Consolidate duplicated inline JS (maintainability)

- **Why not code now:** each page inlines near-identical animation/logic; the
  audit itself scoped this out. It is maintainability-only, with no user-facing
  defect, and touches every page — best done deliberately, not bundled with
  functional work.
- **Recommended action:** optional later refactor to shared logic, only if the
  static architecture is otherwise being revisited.

---

## 4. Suggested sequencing before production

1. **Launch-blocking (mainland production):** H1 ICP filing (§3.1), then the
   footer/placeholder code change (H1 + M6, §3.4).
2. **Correctness / trust:** H3 `llms.txt` (§3.2) and H5 wording (§3.3) — owner
   decisions, then small docs/copy PRs.
3. **Discoverability:** C2 pre-rendering (§3.5), which then unblocks H4 sitemap
   (§3.7).
4. **Polish:** M4 contrast (§3.6), Noto Sans SC self-host (§3.8), L4 cleanup
   (§3.9).

Items 1–2 are the meaningful gates before a mainland-facing launch; the rest can
follow in normal cadence. The client-render blank-page risk (C1) — the single
most severe finding for the target audience — is already resolved.
