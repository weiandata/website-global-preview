# WeianData Website Repository Migration and Refactoring Guide

**Version:** 1.0  
**Status:** Approved  
**Owner:** WeianData  
**Target repository:** `weiandata/website`  
**Repository visibility:** Private  
**Default branch:** `main`

---

## 1. Purpose

This document records the complete process for creating the official WeianData website repository, importing the existing static website files, refactoring the website directory structure, validating the migrated website, and preparing it for deployment.

The website already exists as a complete static website rather than a design-only prototype. The current site consists primarily of:

- Static HTML pages
- Shared JavaScript
- Chinese and English Markdown article libraries
- SEO-related files
- No backend
- No database
- No package manager
- No Node.js build process
- No framework dependency at repository level

The migration goal is therefore not to redesign or rebuild the website, but to:

1. Place the website under version control.
2. Normalize filenames and directory structure.
3. Preserve all existing content and functionality.
4. Remove unsafe or unreliable path conventions.
5. Prepare the repository for deployment to the WeianData server.
6. Keep the repository compatible with the WeianData Engineering Handbook and repository standards.

---

## 2. Completed GitHub Setup

The following steps have already been completed.

### 2.1 GitHub Organization

The official GitHub Organization has been created:

```text
weiandata
```

Organization URL:

```text
https://github.com/weiandata
```

### 2.2 Engineering Infrastructure

The following repositories and standards have already been established:

```text
.github
repository-template
website
```

The `.github` repository contains:

- Organization profile
- Engineering Handbook
- Organization-wide standards
- CI validation
- Security and contribution guidance

The `repository-template` repository is configured as a GitHub Template Repository and provides:

- README
- CHANGELOG
- LICENSE placeholder
- SECURITY policy
- CONTRIBUTING guide
- CODEOWNERS
- Issue templates
- Pull Request template
- Universal `.gitignore`
- Universal `.editorconfig`
- Language-independent CI
- Documentation placeholders
- Example and script placeholders

### 2.3 Website Repository

The official website repository has been created from the template:

```text
weiandata/website
```

Description:

```text
Official website of WeianData.
```

Visibility:

```text
Private
```

Default branch:

```text
main
```

The repository currently inherits the standard structure from `repository-template`.

---

## 3. Existing Website Package

The current website package is a static bilingual website.

Its source package contains approximately:

- 10 HTML pages
- 1 shared JavaScript file
- 80 Chinese Markdown articles
- 80 English Markdown articles
- SEO files
- Supporting assets

The original structure is approximately:

```text
新版本/
├── 首页3a-样本流蓝-v2.dc.html
├── 工具案例.dc.html
├── 方法百科.dc.html
├── 学习中心.dc.html
├── 文章.dc.html
├── Home-EN.dc.html
├── Tools-EN.dc.html
├── Methods-EN.dc.html
├── Learn-EN.dc.html
├── Article-EN.dc.html
├── support.js
├── articles/
│   ├── A01.md ... A30.md
│   └── M01.md ... M50.md
├── articles-en/
│   ├── A01.md ... A30.md
│   └── M01.md ... M50.md
├── robots.txt
├── sitemap.xml
└── llms.txt
```

The exact contents must be preserved during migration.

---

## 4. Important Migration Principles

The migration must follow these principles.

### 4.1 Preserve Behavior

Do not change page behavior, article loading logic, text content, visual design, or navigation semantics unless required for path normalization.

### 4.2 Refactor Structure, Not Product Design

This task is a repository and file-structure refactor.

It is not a visual redesign.

### 4.3 Avoid Broken Links

Every renamed file requires all references to that file to be updated.

Search all:

- HTML files
- JavaScript files
- Markdown files
- sitemap files
- navigation links
- language-switch links
- canonical links

### 4.4 No Client or Sensitive Data

The website repository must not contain:

- Business license scans
- Contracts
- Financial files
- Private customer information
- Personal identity documents
- API keys
- Server passwords
- SSH private keys
- Private email credentials

### 4.5 Preserve Bilingual Content

Chinese and English content must remain separated and easy to maintain.

### 4.6 Keep Deployment Simple

The website is static and should remain deployable through:

- Nginx
- Tencent Cloud lightweight server
- GitHub Actions
- SCP or rsync deployment
- Static hosting if needed later

Do not introduce a frontend framework unless a later redesign explicitly requires one.

---

## 5. Target Repository Structure

After migration, the recommended structure is:

```text
website/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── PULL_REQUEST_TEMPLATE.md
├── articles/
├── articles-en/
├── assets/
│   ├── fonts/
│   ├── images/
│   └── vendor/
├── docs/
├── examples/
├── scripts/
├── en/
│   ├── index.html
│   ├── tools.html
│   ├── methods.html
│   ├── learn.html
│   └── article.html
├── index.html
├── tools.html
├── methods.html
├── learn.html
├── article.html
├── support.js
├── robots.txt
├── sitemap.xml
├── llms.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODEOWNERS
├── PROPRIETARY.md
├── .editorconfig
├── .gitignore
└── .markdownlint-cli2.yaml
```

Notes:

- `index.html` is the Chinese homepage.
- English pages live under `en/`.
- Chinese and English article libraries remain in separate directories.
- Shared runtime files should eventually move into `assets/` where practical.
- The existing template files should be preserved unless they are intentionally adapted for the website project.

---

## 6. File Renaming Plan

The following renaming plan is recommended.

### 6.1 Chinese Pages

| Original file | New file |
| --- | --- |
| `首页3a-样本流蓝-v2.dc.html` | `index.html` |
| `工具案例.dc.html` | `tools.html` |
| `方法百科.dc.html` | `methods.html` |
| `学习中心.dc.html` | `learn.html` |
| `文章.dc.html` | `article.html` |

### 6.2 English Pages

| Original file | New file |
| --- | --- |
| `Home-EN.dc.html` | `en/index.html` |
| `Tools-EN.dc.html` | `en/tools.html` |
| `Methods-EN.dc.html` | `en/methods.html` |
| `Learn-EN.dc.html` | `en/learn.html` |
| `Article-EN.dc.html` | `en/article.html` |

### 6.3 Shared Files

| Original file | Target |
| --- | --- |
| `support.js` | `support.js` initially |
| `articles/` | `articles/` |
| `articles-en/` | `articles-en/` |
| `robots.txt` | `robots.txt` |
| `sitemap.xml` | `sitemap.xml` |
| `llms.txt` | `llms.txt` |

The first migration should minimize risk. Moving `support.js` into `assets/js/` can be handled later after all links are stable.

---

## 7. Step-by-Step Migration Procedure

## Step 1: Clone the Website Repository

Open GitHub Desktop.

Choose:

```text
File
→ Clone Repository
```

Select:

```text
weiandata/website
```

Clone to:

```text
/Users/makunxiang/Developer/WeianData/website
```

The final local path should be:

```text
~/Developer/WeianData/website
```

Open the repository in Visual Studio Code.

---

## Step 2: Back Up the Original Website Package

Before modifying the existing package:

1. Keep the original ZIP unchanged.
2. Create a separate working extraction directory.
3. Do not edit the only copy of the website files.
4. Record the original file count.
5. Record the original directory tree.

Suggested local backup structure:

```text
~/Documents/WeianData-Backups/
└── website-source-v0.3/
```

Do not commit the ZIP archive into Git.

---

## Step 3: Extract the Website Package

Extract the package into a temporary local directory.

Example:

```text
~/Downloads/weiandata-website-import/
```

If the archive produces a malformed directory name such as:

```text
#U65b0#U7248#U672c
```

treat it as the original `新版本` directory.

Do not copy the malformed top-level directory into the repository.

Copy only its contents.

---

## Step 4: Create a Migration Branch

Create a new branch in GitHub Desktop:

```text
refactor/normalize-website-structure
```

Do not perform the entire migration directly on `main`.

This branch isolates:

- File renaming
- Navigation updates
- Link fixes
- SEO updates
- Validation changes

---

## Step 5: Import Content Into the Repository

Copy the website source files into the cloned `website` repository.

Do not overwrite the following template files without review:

```text
.github/
README.md
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
CODEOWNERS
.editorconfig
.gitignore
.markdownlint-cli2.yaml
```

Copy:

```text
HTML pages
support.js
articles/
articles-en/
robots.txt
sitemap.xml
llms.txt
required assets
```

Do not copy:

```text
.DS_Store
ZIP files
temporary files
backup copies
editor caches
private files
```

---

## Step 6: Rename the HTML Pages

Rename the Chinese pages first.

```text
首页3a-样本流蓝-v2.dc.html
→ index.html
```

```text
工具案例.dc.html
→ tools.html
```

```text
方法百科.dc.html
→ methods.html
```

```text
学习中心.dc.html
→ learn.html
```

```text
文章.dc.html
→ article.html
```

Create the directory:

```text
en/
```

Move and rename the English pages:

```text
Home-EN.dc.html
→ en/index.html
```

```text
Tools-EN.dc.html
→ en/tools.html
```

```text
Methods-EN.dc.html
→ en/methods.html
```

```text
Learn-EN.dc.html
→ en/learn.html
```

```text
Article-EN.dc.html
→ en/article.html
```

---

## Step 7: Update Internal Links

Search the entire repository for every original filename.

Use VS Code global search:

```text
Command + Shift + F
```

Search for:

```text
首页3a-样本流蓝-v2.dc.html
工具案例.dc.html
方法百科.dc.html
学习中心.dc.html
文章.dc.html
Home-EN.dc.html
Tools-EN.dc.html
Methods-EN.dc.html
Learn-EN.dc.html
Article-EN.dc.html
```

Replace references carefully.

### Chinese navigation targets

```text
index.html
tools.html
methods.html
learn.html
article.html
```

### English navigation targets

From the Chinese root pages:

```text
en/index.html
en/tools.html
en/methods.html
en/learn.html
en/article.html
```

From pages inside `en/`:

```text
index.html
tools.html
methods.html
learn.html
article.html
```

### Returning from English to Chinese

From pages inside `en/`, Chinese links require:

```text
../index.html
../tools.html
../methods.html
../learn.html
../article.html
```

Relative path handling must be checked page by page.

---

## Step 8: Validate Article Paths

The article-loading logic must continue to locate:

```text
articles/
articles-en/
```

If English pages move to `en/`, relative fetch paths may need to change.

For example, an English page previously using:

```javascript
fetch("articles-en/A01.md")
```

may need:

```javascript
fetch("../articles-en/A01.md")
```

Similarly, shared `support.js` references from English pages may need:

```html
<script src="../support.js"></script>
```

Chinese pages at repository root may continue using:

```html
<script src="support.js"></script>
```

This is one of the highest-risk parts of the migration.

Test every page that dynamically loads Markdown.

---

## Step 9: Review External Dependencies

The current website may load external resources such as:

- React from a CDN
- React DOM from a CDN
- KaTeX from a CDN
- Google Fonts
- Other third-party assets

External resources can cause reliability problems in mainland China.

Document all external dependencies in:

```text
docs/external-dependencies.md
```

For each dependency, record:

- Name
- Version
- URL
- Purpose
- License
- Whether local hosting is recommended

Recommended long-term target:

```text
assets/vendor/
assets/fonts/
```

Do not perform dependency localization in the same commit as the structural migration unless necessary.

Keep this as a separate follow-up task:

```text
refactor/localize-third-party-assets
```

---

## Step 10: Update SEO Files

### `robots.txt`

Verify that:

- Sitemap URL points to the official domain.
- No development paths are exposed.
- Required public pages are crawlable.

Expected sitemap reference:

```text
https://www.weiandata.com/sitemap.xml
```

### `sitemap.xml`

Update all page URLs to reflect the new filenames.

Examples:

```text
https://www.weiandata.com/
https://www.weiandata.com/tools.html
https://www.weiandata.com/methods.html
https://www.weiandata.com/learn.html
https://www.weiandata.com/article.html
https://www.weiandata.com/en/
https://www.weiandata.com/en/tools.html
```

### `llms.txt`

Verify that:

- Company name is correct.
- Domain is correct.
- Main sections match the actual site.
- No obsolete filenames remain.

### Canonical URLs

Check every HTML file for canonical tags.

Update obsolete page names.

---

## Step 11: Update the Website README

The root `README.md` should be customized for the website.

It should contain:

```text
Project overview
Website architecture
Page list
Local preview instructions
Article content structure
Deployment overview
SEO files
Known external dependencies
Security notes
Repository standards
License status
```

Recommended title:

```markdown
# WeianData Website
```

Do not leave the generic repository-template README unchanged.

---

## Step 12: Update Project Metadata

### `CHANGELOG.md`

Add an entry:

```markdown
## [Unreleased]

### Added

- Imported the existing bilingual WeianData website.
- Added Chinese and English article libraries.
- Added SEO and LLM discovery files.

### Changed

- Normalized HTML filenames.
- Moved English pages into the `en/` directory.
- Updated internal navigation and content-loading paths.
```

### License

Because the website source is company-owned and not intended for open-source reuse, replace the generic license placeholder with:

```text
PROPRIETARY.md
```

Recommended notice:

```text
Copyright (c) 2026 WEIAN DATA TECH (Beijing) Co., Ltd.

All rights reserved.

This repository and its contents are proprietary and confidential.
Unauthorized copying, modification, distribution, or use is prohibited.
```

Remove or replace `LICENSE` only after verifying the repository template policy.

### `CODEOWNERS`

Confirm:

```text
* @makunxiang-weiandata
```

or the correct GitHub username.

---

## Step 13: Adapt CI for the Website

The inherited Markdown CI should remain.

Add website-specific validation later, preferably in a separate commit.

Recommended checks:

- Markdown lint
- Broken local links
- HTML syntax
- Missing referenced files
- Duplicate IDs
- Invalid relative paths
- sitemap XML validity
- robots.txt existence
- required page existence

The website does not currently need:

- npm install
- Node.js build
- framework build
- language-specific tests

Do not introduce package managers solely for validation unless justified.

---

## Step 14: Local Preview

Use a local static server.

Do not test only by double-clicking HTML files because browser file restrictions can break `fetch()`.

From the repository root, run one of the following.

### Python

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

### Alternative

Use the VS Code Live Server extension if already approved.

Python's built-in server is sufficient and avoids additional dependencies.

---

## Step 15: Manual Functional Testing

Test all primary pages.

### Chinese

- Homepage
- Tools
- Methods
- Learn
- Article

### English

- Homepage
- Tools
- Methods
- Learn
- Article

### Required checks

- Navigation works
- Language switching works
- Article lists load
- Individual Markdown articles load
- Internal links work
- No console errors
- No missing resources
- Mobile layout remains usable
- Fonts render acceptably
- Equations render if KaTeX is used
- Contact email is correct
- Domain links are correct

Open browser developer tools and check:

```text
Console
Network
```

There should be no unexpected 404 errors.

---

## Step 16: Automated Link Search

Before commit, search for obsolete names.

The following searches must return zero results:

```text
首页3a-样本流蓝-v2.dc.html
工具案例.dc.html
方法百科.dc.html
学习中心.dc.html
文章.dc.html
Home-EN.dc.html
Tools-EN.dc.html
Methods-EN.dc.html
Learn-EN.dc.html
Article-EN.dc.html
```

Also search for:

```text
localhost
127.0.0.1
/Users/
file://
```

These should not appear in production files.

---

## Step 17: Commit Strategy

Use multiple logical commits rather than one huge commit.

Recommended sequence:

### Commit 1

```text
feat: import bilingual website source
```

### Commit 2

```text
refactor: normalize website file structure
```

### Commit 3

```text
fix: update navigation and article paths
```

### Commit 4

```text
docs: document website development workflow
```

### Commit 5

```text
ci: add static website validation
```

Do not mix dependency localization into these commits.

---

## Step 18: Pull Request

Create a Pull Request from:

```text
refactor/normalize-website-structure
```

to:

```text
main
```

PR title:

```text
feat: import and normalize official website
```

PR description should include:

- Source package imported
- Pages renamed
- English pages moved
- Navigation updated
- Article loading validated
- SEO files updated
- Local preview tested
- Known follow-up items

Even in the founder-only stage, this migration should use a PR because it is a large structural change.

---

## Step 19: Acceptance Criteria

The migration is complete only when all requirements below are met.

### Repository

- [ ] Website repository is private.
- [ ] Repository is cloned to the standard local path.
- [ ] Migration occurs on a dedicated branch.
- [ ] Template governance files remain present.

### Structure

- [ ] Chinese homepage is `index.html`.
- [ ] English homepage is `en/index.html`.
- [ ] English pages are under `en/`.
- [ ] Article directories are preserved.
- [ ] No malformed archive directory name remains.
- [ ] No obsolete `.dc.html` filenames remain unless explicitly retained.

### Functionality

- [ ] All Chinese pages load.
- [ ] All English pages load.
- [ ] Navigation works.
- [ ] Language switching works.
- [ ] Markdown articles load.
- [ ] No unexpected 404 errors.
- [ ] No critical console errors.

### SEO

- [ ] `robots.txt` is valid.
- [ ] `sitemap.xml` uses normalized URLs.
- [ ] `llms.txt` reflects current content.
- [ ] Canonical URLs are correct.
- [ ] Official domain is consistently used.

### Security

- [ ] No secrets committed.
- [ ] No private customer data committed.
- [ ] No business license or contract files committed.
- [ ] No local absolute paths committed.
- [ ] Repository uses a proprietary notice.

### Documentation

- [ ] README is website-specific.
- [ ] CHANGELOG is updated.
- [ ] External dependencies are documented.
- [ ] Deployment process is documented or tracked as a follow-up.

### Git

- [ ] Commits are logically separated.
- [ ] CI passes.
- [ ] Pull Request is reviewed.
- [ ] Branch is deleted after merge.

---

## 20. Deployment Preparation

The website will ultimately be deployed to the WeianData server.

Known infrastructure:

```text
Domain: weiandata.com
Server: Tencent Cloud lightweight application server
Deployment type: Static website
Web server: Nginx recommended
```

Deployment should be handled in a separate phase after repository migration.

Recommended future deployment flow:

```text
Push to main
→ GitHub Actions validation
→ Secure deployment
→ Tencent Cloud server
→ Nginx static root
→ HTTPS
→ Production verification
```

Do not store server credentials in the repository.

Use GitHub Actions Secrets or a secure deployment mechanism.

---

## 21. Follow-Up Tasks

The following tasks should be handled after the initial repository migration.

### Priority 1

- Localize high-risk CDN dependencies.
- Verify website behavior in mainland China.
- Complete ICP filing.
- Replace ICP placeholders.
- Add public security filing information.
- Configure HTTPS.

### Priority 2

- Add HTML and link validation CI.
- Add deployment workflow.
- Add cache headers.
- Add error page.
- Add favicon and web manifest checks.
- Validate accessibility.

### Priority 3

- Evaluate clean URLs.
- Evaluate conversion to a static site generator.
- Evaluate content management workflow.
- Add analytics only after privacy review.

Do not introduce major architectural changes before the current static site has been successfully migrated and deployed.

---

## 22. Final Recommended Workflow

```text
Preserve original package
→ Clone website repository
→ Create migration branch
→ Import source files
→ Normalize names and structure
→ Update links
→ Validate article loading
→ Update SEO files
→ Customize documentation
→ Run local server
→ Complete manual tests
→ Run automated validation
→ Commit in logical units
→ Open Pull Request
→ Merge to main
→ Configure deployment
```

---

## 23. Summary

The WeianData website is already a complete static bilingual website.

The correct next step is not a redesign.

The correct next step is to place the site under disciplined version control, normalize its structure, validate all relative paths, preserve its bilingual content, and prepare it for stable deployment.

The migration must remain conservative:

- Preserve content
- Preserve behavior
- Improve structure
- Improve reliability
- Avoid unnecessary frameworks
- Avoid unnecessary dependencies
- Keep deployment simple

---

© WeianData

This document defines the approved migration and refactoring process for the official WeianData website repository.
