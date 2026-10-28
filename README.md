# WeianData Website

Official trilingual (English, Chinese, German) website for WeianData. This repository contains the complete
static site, its English, Chinese, and German article libraries, and the files required
for search-engine and LLM discovery.

Status: Active

Owner: WeianData

Production domain: <https://global.weiandata.com>

## Architecture

The site deliberately has no backend, database, framework-level build, package
manager, or repository-level runtime dependency.

```text
.
├── articles/       # Chinese Markdown articles: A01-A30 and M01-M50
├── articles-en/    # English Markdown articles: A01-A30 and M01-M50
├── articles-de/    # German Markdown articles: A01-A30 and M01-M50
├── assets/         # Reserved for locally hosted fonts, images, and vendors
├── docs/           # Architecture, dependency, migration, and deployment docs
├── zh/             # Chinese HTML pages
├── de/             # German HTML pages
├── scripts/        # Repository validation utilities
├── index.html      # English homepage (site default)
├── tools.html
├── methods.html
├── learn.html
├── article.html
├── support.js      # Shared browser runtime
├── robots.txt
├── sitemap.xml
└── llms.txt
```

## Pages

| English (default)              | Chinese                           | German                            |
| ------------------------------ | --------------------------------- | --------------------------------- |
| [Home](index.html)             | [Home](zh/index.html)             | [Home](de/index.html)             |
| [Tools and cases](tools.html)  | [Tools and cases](zh/tools.html)  | [Tools and cases](de/tools.html)  |
| [Methods](methods.html)        | [Methods](zh/methods.html)        | [Methods](de/methods.html)        |
| [Learning hub](learn.html)     | [Learning hub](zh/learn.html)     | [Learning hub](de/learn.html)     |
| [Article reader](article.html) | [Article reader](zh/article.html) | [Article reader](de/article.html) |

## Local Preview

Serve the repository over HTTP so browser security rules do not block Markdown
article loading:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Do not validate article loading by opening
the HTML files directly from the filesystem.

## Article Content

Chinese content lives in `articles/`, English content in `articles-en/`, and German content in `articles-de/`.
Both libraries use matching identifiers:

- `A01.md` through `A30.md` for long-form articles.
- `M01.md` through `M50.md` for methods notes.

The article readers select content with an `id` query parameter, for example
`/article?id=A01` (English), `/zh/article?id=A01` (Chinese), and `/de/article?id=A01` (German). Keep identifiers aligned
between languages when adding or renaming content.

## Validation

Run the dependency-free repository checks from the project root:

```bash
python3 scripts/validate_site.py
```

The validator checks required files, article inventories, local HTML links,
duplicate IDs, canonical URLs, sitemap XML, SEO paths, and unsafe local path
references. Browser-level navigation and article loading should also be checked
through a local HTTP server before release.

## Deployment

Source is hosted in GitHub and production is published outside mainland China
through Cloudflare Pages' native Git integration. Pages runs
`python3 scripts/build_release.py --output dist` and publishes `dist`. The
release builder copies only public website files, including the Pages
`_headers` and `_redirects` policies; repository documentation and development files are excluded.
See [deployment guidance](docs/deployment.md) for the exact dashboard, domain,
branch, verification, and rollback settings.

## SEO and Discovery

- `robots.txt` publishes the production sitemap location.
- `sitemap.xml` lists the five normalized routes in all three languages (English at the root, Chinese under `/zh/`, German under `/de/`).
- `llms.txt` describes the company and public website sections.
- Every HTML page declares a canonical URL on `global.weiandata.com`.

Update these files together whenever a public route changes.

## External Dependencies

Runtime dependencies and their hosting locations are documented in
[external dependencies](docs/external-dependencies.md). React, React DOM, and
KaTeX are served from this site, and so is the Noto Sans SC web font; the
site makes no runtime request to Google Fonts.

## Security

This repository must not contain credentials, server keys, private customer
data, identity documents, contracts, financial files, or production datasets.
Use GitHub Actions secrets or another approved secret store for future
deployment credentials. Report vulnerabilities according to
[SECURITY.md](SECURITY.md).

## Repository Standards

Changes use short-lived branches and pull requests. Follow
[CONTRIBUTING.md](CONTRIBUTING.md), [CODEOWNERS](CODEOWNERS), and the
[repository standard](docs/repository-standard.md). Keep the static architecture
unless a separately reviewed redesign approves a different approach.

## License

Copyright (c) 2026 WEIAN DATA TECH (Beijing) Co., Ltd.
(惟安数据科技（北京）有限公司). All rights reserved. This repository is
proprietary; see [PROPRIETARY.md](PROPRIETARY.md). Licensing and permission
requests: <contact@weiandata.com>.

## Official Website

https://global.weiandata.com
