# External Dependencies

The website is static, but its shared browser runtime and article pages load the
resources below at runtime. Versions and URLs are recorded so availability,
licensing, and localization can be reviewed independently of the structural
migration.

| Dependency | Version | Runtime URL | Purpose | License | Local hosting |
| --- | --- | --- | --- | --- | --- |
| Noto Sans SC | CDN family request; not pinned | `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap` | Chinese-capable web font | SIL Open Font License 1.1 | Still CDN — the only remaining external runtime request; falls back to the system CJK stack. Self-hosting a subset is a follow-up |
| KaTeX | 0.16.9 | `/assets/vendor/katex/katex.min.css` and `katex.min.js` (vendored; was jsDelivr) | Render equations in article pages | MIT | **Localized** — CSS trimmed to woff2; 20 fonts under `assets/vendor/katex/fonts/` |
| Babel Standalone | 7.29.0 | `https://unpkg.com/@babel/standalone@7.29.0/babel.min.js` | Compile JSX only when a page uses a JSX `x-import`; no current page does, so it is never fetched at runtime | MIT | Only needed if JSX imports are later introduced |
| React | 18.3.1 | `/assets/vendor/react.production.min.js` (vendored; was unpkg) | Component runtime | MIT | **Localized** — served same-origin with the original SRI hash |
| React DOM | 18.3.1 | `/assets/vendor/react-dom.production.min.js` (vendored; was unpkg) | Browser rendering for React components | MIT | **Localized** — served same-origin with the original SRI hash |

The links to CRAN on the tools pages are ordinary outbound links, not runtime
dependencies.

## Operational Notes

- React, React DOM, and KaTeX are vendored under `assets/vendor/` and served
  same-origin, so no third-party CDN is required to render pages or equations —
  the main mainland-China reliability risk is removed.
- Google Fonts (Noto Sans SC) is the only remaining external runtime request; a
  blocked request falls back to the system CJK font stack (`PingFang SC`,
  `Microsoft YaHei`).
- If the React runtime still fails to load or boot, `support.js` now reveals the
  raw inline-styled markup so the page degrades to readable static content
  instead of a blank page.
- Babel Standalone is fetched on demand only for JSX `x-import`s; the current
  site uses none, so it is not loaded in practice and its availability does not
  affect rendering.
- Vendored assets retain their upstream version and license; React and React DOM
  keep their original Subresource Integrity hashes (verified byte-identical to
  the CDN copies).
- Remaining follow-up: self-host a subsetted Noto Sans SC under `assets/fonts/`.
