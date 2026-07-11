# Cloudflare Pages deployment

The repository is hosted on GitHub. Cloudflare Pages uses its native GitHub
integration to build and publish the static site outside mainland China. There
is no origin server, Nginx instance, database, package install, deployment
token, or GitHub Actions deployment workflow.

Use the standard global Pages service only. Do not enable the separate
Cloudflare China Network product for this zone; Pages is not a mainland-China
hosting service, and China Network has separate Enterprise, ICP, and content
review prerequisites.

## Pages project settings

Create a Pages project from the GitHub repository and use these values:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | None |
| Root directory | `/` (repository root) |
| Build command | `python3 scripts/validate_site.py && python3 scripts/build_release.py --output dist` |
| Build output directory | `dist` |
| Environment variables | None |

Enable automatic production deployments for `main`. Enable preview deployments
for non-production branches used by pull requests. Cloudflare injects its own
`CF_PAGES*` variables; this site does not currently consume them.

The build command creates a minimal public artifact instead of publishing the
repository root. This prevents `.git`, documentation, deployment notes, and
developer scripts from becoming public files. A failed validation or build
returns a non-zero exit status and stops the Pages deployment.

## Domain and DNS

Add `global.weiandata.com` as the production custom domain in the Pages project.
Because it is a subdomain, Pages can create the CNAME automatically when the
`weiandata.com` zone is in the same Cloudflare account. If DNS is hosted
elsewhere, first associate the custom domain in Pages and then point the
`global` CNAME to the assigned `<project>.pages.dev` hostname. Cloudflare
provisions and renews TLS; no certificate or private key belongs in this
repository.

After the custom domain is active, add another Bulk Redirect from the production
`<project>.pages.dev` hostname to `https://global.weiandata.com`, preserving paths
and query strings. The checked-in `_headers` file independently marks all
`pages.dev` and branch-preview responses `noindex` to avoid duplicate indexing.

## Routing, headers, and caching

Cloudflare Pages automatically serves the top-level `404.html` with a real 404
response. It also exposes HTML files as clean routes (for example,
`tools.html` becomes `/tools`), so canonical and sitemap URLs use the clean
form while old `.html` links continue to redirect.

`_headers` adds clickjacking, MIME-sniffing, referrer, browser-permission, and
preview-indexing protections. It intentionally does not add a Content Security
Policy because the current pages contain inline scripts and runtime evaluation.
It also does not override caching: Pages already uses ETags, compression, and
its distributed cache, and custom cache rules can serve stale deployments.

## Release flow

1. Open a pull request and let Cloudflare create a preview deployment.
2. Run `python3 scripts/validate_site.py` locally and test navigation and article
   loading through an HTTP server.
3. Merge the reviewed commit into `main`.
4. Confirm that the Pages production deployment built the expected commit.
5. Verify `/` (English), `/zh/`, the eight clean page routes, the legacy
   `/en/*` 301 redirects, article loading, SEO files,
   the custom 404 status, response headers, custom-domain DNS, and the
   `pages.dev` redirect.

Cloudflare Pages deployments are immutable. To roll back, select a previously
successful production deployment in the Pages dashboard and choose **Rollback**.
No DNS, server, or certificate change should be part of an ordinary rollback.

## Cloudflare references

- [GitHub integration](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/)
- [Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Headers](https://developers.cloudflare.com/pages/configuration/headers/)
- [Serving Pages and clean routes](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- [Production rollbacks](https://developers.cloudflare.com/pages/configuration/rollbacks/)
- [China Network prerequisites](https://developers.cloudflare.com/china-network/get-started/)

## Secrets and regional scope

The current build needs no secrets. If a future build adds credentials, store
them as encrypted Pages environment variables with least privilege; never
commit them. Because production is published outside mainland China rather than
from a mainland hosting provider, the former ICP filing gate and placeholder
footer have been removed. Reassess regulatory and network requirements before
adding a mainland origin or mainland-specific delivery product.
