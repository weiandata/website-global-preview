# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- State on the Home pages and in `llms.txt` that all four in-house R packages
  are published on CRAN, and replace the validator rule that banned CRAN copy
  there with checks for CRAN links and install snippets on the Tools pages.

### Added

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
