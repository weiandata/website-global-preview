# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Correct article errors in the Chinese and English sources. A04 now installs
  IRTC from CRAN and uses its real API (`irtc()`, `plain_summary()`,
  `irtc_param_table()`, `irtc.mml.2pl()`), replacing the outdated GitHub
  install, version, license, and functions that do not exist; its subsample
  size reads 10,000–50,000. Other IRTC mentions point to CRAN and drop the stale
  "26 test groups". References to the unpublished Q&A series are removed.
- Fix English mistranslations: GRM is the Graded Response Model; DIF is
  Differential Item Functioning; SESOI is the smallest effect size of interest;
  θ comparability is across calibrations, not items; Chinese-only artifacts
  (character counts, duplicated names, pinyin mnemonics) are rewritten.
- The German A04 expert example uses `irtc.mml.2pl()`; `irtc.mml()` with
  `irtmodel = "GPCM"` silently fits a PCM.
- Draw the home hero pipeline as a still frame for reduced-motion visitors;
  it previously rendered blank because resizing cleared the canvas.

### Added

- Add a German version: five pages under `/de/` and all 80 articles in
  `articles-de/`, with German titles in the Learning hub and article reader.
- Replace the single language toggle with an EN / 中文 / DE switch on every
  page, and add `de` hreflang alternates, `de_DE` Open Graph locales, German
  sitemap URLs, and German sections in `llms.txt` and `llms-full.txt`.
- Self-host Noto Sans SC (OFL) under `assets/fonts/`, so no visitor request
  reaches Google Fonts; the validator now rejects Google Fonts references.
- Add a German Impressum (`de/impressum.html`, § 5 DDG) with the provider
  details from the business licence, linked from every page footer; the
  validator checks the link and the required details.
- Add a German privacy notice (`de/datenschutz.html`, GDPR Art. 13): no
  cookies or tracking, Cloudflare hosting and connection data, contact
  requests, and visitor rights; linked from every page footer and checked by
  the validator.
- State each package's minimum R version (from its CRAN `Depends`) under its
  install snippet on the Tools pages, and validate it.
- Add copyable `install.packages()` / `library()` R snippets for DCC, IRTC,
  WFC, and LISTC to the bilingual Tools pages.
- Link the WeianData AI Skills site from the footer of every bilingual page.
- Add the DCC CRAN release link and state that DCC, IRTC, WFC, and LISTC are
  all published on CRAN.
- Add an in-development preview of Ogive, the macOS IRT application, to the
  bilingual Home and Tools pages.
- Add LISTC as the fourth in-house tool case on the bilingual Tools pages, and
  extend the workflow chain to `cleaning -> modeling -> weighting -> reporting`.
- Add CRAN release links for IRTC, WFC, and LISTC, and a source link for DCC,
  on the bilingual Tools pages.
- Import the existing bilingual WeianData website.
- Add Chinese and English article libraries.
- Add SEO and LLM discovery files.
- Add static-site validation and website-specific documentation.

### Changed

- Align the global English (`/`) and Chinese (`/zh/`) homepage copy with the
  www homepages.
- Polish layout on both languages: align the header with the content column,
  line up service rows, pin tool-card links to the card bottom, turn the Ogive
  teaser into a slim preview bar, move each CRAN link into its install snippet,
  and balance heading line breaks.
- On phones, fit the header nav on one row with the language switch beside the
  logo, and show the home stats as a 2 × 2 grid.
- State on the Home pages and in `llms.txt` that all four in-house R packages
  are published on CRAN, and replace the validator rule that banned CRAN copy
  there with checks for CRAN links and install snippets on the Tools pages.
- Standardize the legal owner identity and licensing contact, and apply the
  company proprietary-license profile to the repository and website content.
- Normalize Chinese HTML filenames.
- Move English pages into the `en/` directory.
- Update navigation, article-loading, canonical, and sitemap paths.

## [1.0.0] - 2026-07-10

### Added

- Establish the language-independent WeianData repository template.
- Add governance, contribution, security, ownership, and versioning documents.
- Add issue and pull request templates.
- Add Markdown and link validation workflow.
- Add documentation, examples, and scripts guidance.
