# DCC–IRTC–WFC Case and Site Synchronization Design

## Objective

Update both bilingual website repositories so the public project portfolio is
consistently presented as DCC, IRTC, and WFC. Bring the mobile portrait-browser
adaptation and approved homepage copy changes from `website-global-preview`
back into `website` without copying international-only routing, metadata, or
deployment behavior.

The two repositories remain independent static sites:

- `website` serves Chinese by default at `www.weiandata.com` and English under
  `/en/`, using `.html` routes and the mainland-China deployment configuration.
- `website-global-preview` serves English by default at
  `global.weiandata.com` and Chinese under `/zh/`, using its Cloudflare Pages
  routing conventions.

## Public Case Narrative

The three cases form a coherent survey and assessment workflow:

1. **DCC — data cleaning:** rule-driven detection, controlled execution,
   cell-level audit trails, reporting, tracing, and reproducible reruns.
2. **IRTC — measurement modeling:** marginal maximum-likelihood IRT estimation,
   broad item-model coverage, scalable computation, and controlled-accuracy
   options with exact computation as the default.
3. **WFC — survey weighting:** precheck-first target construction, raking and
   post-stratification, category-collapse review, diagnostics, and auditable
   workflow records.

Chinese and English copy will be written separately but convey the same facts.
The DCC, IRTC, and WFC repository READMEs are the factual sources. Copy will
avoid mutable test counts, unverified performance superlatives, and release
claims that could quickly become stale.

## Page Changes

In both languages of both repositories:

- Replace the homepage case cards and their anchors with DCC, IRTC, and WFC in
  that order.
- Replace the tools/cases page flow, detailed case sections, headings, tags,
  calls to action, and internal anchors with the same three projects.
- Reframe the old “modeling → weighting → merging” story as “cleaning →
  modeling → weighting.”
- Update descriptions and discovery content that explicitly advertise the old
  IRTC, ratecalib, and mergecalib portfolio, including page metadata, social
  sharing metadata, JSON-LD descriptions, and LLM-facing site summaries where
  present.
- Remove stale homepage and case-page links to `#ratecalib` and `#mergecalib`.

The visual language, case-section layout, colors, typography, and overall
information architecture remain unchanged. No new image assets or runtime
dependencies are required.

## Mobile and Copy Synchronization

`website-global-preview/assets/css/mobile.css` is the source of truth for the
phone-only portrait-browser behavior. Copy it to `website/assets/css/mobile.css`
and reference it from every production HTML page in both languages, plus the
404 page. References must use paths appropriate to the page depth.

The mobile stylesheet remains scoped to `@media (max-width: 768px)` and must
preserve desktop rendering. It covers horizontal-overflow prevention, compact
gutters and headers, collapsed grids, readable timelines and diagrams,
non-sticky case headers, mobile anchor offsets, and scrollable tables, code,
and display math.

The approved international-site homepage wording is also the source for the
corresponding Chinese and English homepage body copy in `website`. This applies
to the revised hero/theme wording and five-step engagement process. The copy is
transferred semantically, while repository-specific paths and legal text stay
unchanged.

## Repository-Specific Boundaries

The synchronization must not overwrite:

- canonical URLs, `hreflang` URLs, Open Graph URLs, or JSON-LD page URLs;
- Chinese-site `.html` paths or international-site clean routes;
- language-switch and article-fetch paths;
- `website` ICP filing text, MIIT link, Nginx configuration, or mainland-China
  release workflow;
- `website-global-preview` Cloudflare Pages files, Google site verification,
  redirects, headers, or international copyright footer;
- repository-specific sitemap, robots, release-builder, and validator rules
  unless a case-content reference in those files must be updated.

## Validation

Implementation is complete only when:

- `python3 scripts/validate_site.py` passes in both repositories;
- the production-mode validator for `website` is run and any failure caused by
  pre-existing placeholder filing data is reported separately from this work;
- all production pages link to the mobile stylesheet at an existing local path;
- homepage cards and tools-page anchors resolve to unique DCC, IRTC, and WFC
  sections in both languages of both repositories;
- targeted searches find no remaining portfolio presentation or anchors for
  `ratecalib` or `mergecalib` on home or tools pages;
- desktop and narrow portrait rendering are checked for the home and tools
  pages in Chinese and English, with no horizontal page overflow and no
  overlapping case or process content;
- site-specific domains, routes, language switches, legal footers, and article
  loading behavior remain valid.

## Out of Scope

- Changing the DCC, IRTC, or WFC package repositories.
- Redesigning the website or replacing the dependency-free static architecture.
- Removing ratecalib or mergecalib references from educational articles where
  they are discussed as tools rather than featured company cases.
- Making the two deployment stacks identical.
