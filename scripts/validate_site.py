#!/usr/bin/env python3
"""Validate the dependency-free WeianData static website repository."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ROOT_PAGES = ["index.html", "tools.html", "methods.html", "learn.html", "article.html"]
ZH_PAGES = [f"zh/{name}" for name in ROOT_PAGES]
DE_PAGES = [f"de/{name}" for name in ROOT_PAGES]
HTML_PAGES = ROOT_PAGES + ZH_PAGES + DE_PAGES
ARTICLE_DIRECTORIES = ("articles", "articles-en", "articles-de")
# Every page links its counterparts in all site languages.
HREFLANGS = ("en", "zh-CN", "de", "x-default")
FEATURED_CASE_IDS = ("dcc", "irtc", "wfc", "listc")
CRAN_PACKAGES = ("DCC", "IRTC", "WFC", "LISTC")
# Minimum R version each package declares on CRAN (Depends: R (>= x)).
CRAN_R_REQUIREMENTS = {"DCC": "4.1", "IRTC": "3.5.0", "WFC": "3.6.0", "LISTC": "4.1"}
LEGACY_CASE_IDS = ("ratecalib", "mergecalib")
EXPECTED_ARTICLES = {
    *(f"A{number:02}.md" for number in range(1, 31)),
    *(f"M{number:02}.md" for number in range(1, 51)),
}
EXPECTED_CANONICALS = {
    "index.html": "https://global.weiandata.com/",
    "tools.html": "https://global.weiandata.com/tools",
    "methods.html": "https://global.weiandata.com/methods",
    "learn.html": "https://global.weiandata.com/learn",
    "article.html": "https://global.weiandata.com/article",
    "zh/index.html": "https://global.weiandata.com/zh/",
    "zh/tools.html": "https://global.weiandata.com/zh/tools",
    "zh/methods.html": "https://global.weiandata.com/zh/methods",
    "zh/learn.html": "https://global.weiandata.com/zh/learn",
    "zh/article.html": "https://global.weiandata.com/zh/article",
    "de/index.html": "https://global.weiandata.com/de/",
    "de/tools.html": "https://global.weiandata.com/de/tools",
    "de/methods.html": "https://global.weiandata.com/de/methods",
    "de/learn.html": "https://global.weiandata.com/de/learn",
    "de/article.html": "https://global.weiandata.com/de/article",
}
OBSOLETE_NAMES = (
    "首页3a-样本流蓝-v2.dc" + ".html",
    "工具案例.dc" + ".html",
    "方法百科.dc" + ".html",
    "学习中心.dc" + ".html",
    "文章.dc" + ".html",
    "Home-EN.dc" + ".html",
    "Tools-EN.dc" + ".html",
    "Methods-EN.dc" + ".html",
    "Learn-EN.dc" + ".html",
    "Article-EN.dc" + ".html",
)
FORBIDDEN_PRODUCTION_REFERENCES = ("localhost", "127.0.0.1", "/Users/", "file://")
# Fonts are self-hosted so no visitor request reaches Google (GDPR exposure for EU visitors).
FORBIDDEN_FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")
# German law (§ 5 DDG) requires a provider notice reachable from every page.
IMPRESSUM_PAGE = "de/impressum.html"
IMPRESSUM_REQUIRED_TEXT = ("§ 5 DDG", "91110112MAKGCAAW6F", "contact@weiandata.com", "tel:+8613161314675", "101199", "Ma Kunxiang")


class PageParser(HTMLParser):
    """Collect links, element IDs, and canonical URLs from one HTML page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.ids: list[str] = []
        self.canonicals: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append(value)
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonicals.append(values["href"])


def production_text_files() -> list[Path]:
    files = [ROOT / name for name in (*HTML_PAGES, IMPRESSUM_PAGE)]
    files.extend(ROOT / name for name in ("support.js", "robots.txt", "sitemap.xml", "llms.txt"))
    for directory in ARTICLE_DIRECTORIES:
        files.extend(sorted((ROOT / directory).glob("*.md")))
    return files


def validate_required_files(errors: list[str]) -> None:
    required = [
        *HTML_PAGES,
        IMPRESSUM_PAGE,
        "support.js",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "README.md",
        "_headers",
        ".gitignore",
        "PROPRIETARY.md",
        "assets/fonts",
        "assets/images",
        "assets/vendor",
        "docs/external-dependencies.md",
        "docs/deployment.md",
        "scripts/build_release.py",
    ]
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required path: {relative}")

    obsolete_files = sorted(path.relative_to(ROOT) for path in ROOT.rglob("*.dc.html"))
    if obsolete_files:
        errors.append(f"Obsolete .dc.html files remain: {', '.join(map(str, obsolete_files))}")


def validate_article_inventory(errors: list[str]) -> None:
    for directory in ARTICLE_DIRECTORIES:
        actual = {path.name for path in (ROOT / directory).glob("*.md")}
        missing = sorted(EXPECTED_ARTICLES - actual)
        extra = sorted(actual - EXPECTED_ARTICLES)
        if missing:
            errors.append(f"{directory} is missing: {', '.join(missing)}")
        if extra:
            errors.append(f"{directory} has unexpected Markdown files: {', '.join(extra)}")


def validate_production_text(errors: list[str]) -> None:
    for path in production_text_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for name in OBSOLETE_NAMES:
            if name in text:
                errors.append(f"{relative} references obsolete filename {name}")
        for value in FORBIDDEN_PRODUCTION_REFERENCES:
            if value in text:
                errors.append(f"{relative} contains forbidden production reference {value}")

    if "fetch('articles-en/' + id + '.md')" not in (ROOT / "article.html").read_text(encoding="utf-8"):
        errors.append("English article reader does not fetch from articles-en/")
    if "fetch('../articles/' + id + '.md')" not in (ROOT / "zh/article.html").read_text(encoding="utf-8"):
        errors.append("Chinese article reader does not fetch from ../articles/")
    if "fetch('../articles-de/' + id + '.md')" not in (ROOT / "de/article.html").read_text(encoding="utf-8"):
        errors.append("German article reader does not fetch from ../articles-de/")

    for relative in [*HTML_PAGES, IMPRESSUM_PAGE, "404.html"]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for host in FORBIDDEN_FONT_HOSTS:
            if host in text:
                errors.append(f"{relative} requests fonts from {host}; use assets/fonts/noto-sans-sc.css")


def local_target(page: Path, reference: str) -> Path | None:
    parts = urlsplit(reference)
    if parts.scheme or parts.netloc or reference.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    path = unquote(parts.path)
    if not path:
        return None
    target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/"):
        target /= "index.html"
    return target.resolve()


def validate_html(errors: list[str]) -> None:
    for relative in HTML_PAGES:
        page = ROOT / relative
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()

        duplicate_ids = sorted({element_id for element_id in parser.ids if parser.ids.count(element_id) > 1})
        if duplicate_ids:
            errors.append(f"{relative} has duplicate IDs: {', '.join(duplicate_ids)}")

        expected_canonical = EXPECTED_CANONICALS[relative]
        if parser.canonicals != [expected_canonical]:
            errors.append(
                f"{relative} canonical is {parser.canonicals!r}; expected {[expected_canonical]!r}"
            )

        for reference in parser.references:
            target = local_target(page, reference)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{relative} links outside repository: {reference}")
                continue
            if not target.exists():
                errors.append(f"{relative} has missing local reference: {reference}")

        text = page.read_text(encoding="utf-8")
        for hreflang in HREFLANGS:
            if f'hreflang="{hreflang}"' not in text:
                errors.append(f"{relative} lacks a hreflang=\"{hreflang}\" alternate")
        if text.count("data-lang-switch") < 1 or 'aria-current="page"' not in text:
            errors.append(f"{relative} lacks the EN / 中文 / DE language switch")
        if not any(
            local_target(page, reference) == (ROOT / IMPRESSUM_PAGE).resolve() for reference in parser.references
        ):
            errors.append(f"{relative} does not link the Impressum")

    impressum = (ROOT / IMPRESSUM_PAGE).read_text(encoding="utf-8")
    for required in IMPRESSUM_REQUIRED_TEXT:
        if required not in impressum:
            errors.append(f"{IMPRESSUM_PAGE} lacks required provider detail {required!r}")


def validate_featured_cases(errors: list[str]) -> None:
    for relative in ("index.html", "zh/index.html", "de/index.html"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        positions = [text.find(f'tools.html#{case_id}') for case_id in FEATURED_CASE_IDS]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append(f"{relative} does not present {', '.join(CRAN_PACKAGES)} in order")
        for case_id in LEGACY_CASE_IDS:
            if f"tools.html#{case_id}" in text:
                errors.append(f"{relative} still links featured case {case_id}")

    for relative in ("tools.html", "zh/tools.html", "de/tools.html"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        positions = [text.find(f'id="{case_id}"') for case_id in FEATURED_CASE_IDS]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append(f"{relative} does not define {', '.join(CRAN_PACKAGES)} in order")
        for case_id in LEGACY_CASE_IDS:
            if f'id="{case_id}"' in text or f'href="#{case_id}"' in text:
                errors.append(f"{relative} still presents featured case {case_id}")


def validate_retired_project_references(errors: list[str]) -> None:
    for path in production_text_files():
        text = path.read_text(encoding="utf-8").lower()
        relative = path.relative_to(ROOT)
        for name in LEGACY_CASE_IDS:
            if name in text:
                errors.append(f"{relative} still references retired featured project {name}")

    for relative in ("tools.html", "zh/tools.html", "de/tools.html"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        for package in CRAN_PACKAGES:
            if f'href="https://CRAN.R-project.org/package={package}"' not in text:
                errors.append(f"{relative} is missing the CRAN link for {package}")
            if f'"{package}"</span>)' not in text or f"library({package})" not in text:
                errors.append(f"{relative} is missing the R install snippet for {package}")
            start = text.find(f'id="{package.lower()}"')
            case = text[start:text.find("</article>", start)] if start >= 0 else ""
            if f'data-r-requires="{CRAN_R_REQUIREMENTS[package]}"' not in case:
                errors.append(f"{relative} does not state R >= {CRAN_R_REQUIREMENTS[package]} for {package}")


def validate_seo(errors: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    try:
        document = ET.parse(sitemap)
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml is invalid XML: {exc}")
        return

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    actual_urls = {node.text for node in document.findall("sm:url/sm:loc", namespace)}
    article_ids = [f"A{n:02}" for n in range(1, 31)] + [f"M{n:02}" for n in range(1, 51)]
    expected_urls = set(EXPECTED_CANONICALS.values())
    expected_urls.update(f"https://global.weiandata.com/article?id={i}" for i in article_ids)
    expected_urls.update(f"https://global.weiandata.com/zh/article?id={i}" for i in article_ids)
    expected_urls.update(f"https://global.weiandata.com/de/article?id={i}" for i in article_ids)
    if actual_urls != expected_urls:
        errors.append(
            "sitemap.xml URLs differ from canonical URLs: "
            f"missing={sorted(expected_urls - actual_urls)}, extra={sorted(actual_urls - expected_urls)}"
        )

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://global.weiandata.com/sitemap.xml" not in robots:
        errors.append("robots.txt does not publish the production sitemap URL")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_article_inventory(errors)
    validate_production_text(errors)
    validate_html(errors)
    validate_featured_cases(errors)
    validate_retired_project_references(errors)
    validate_seo(errors)
    if errors:
        print("Static website validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Static website validation passed: "
        f"{len(HTML_PAGES)} HTML pages and {len(EXPECTED_ARTICLES) * len(ARTICLE_DIRECTORIES)} Markdown articles."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
