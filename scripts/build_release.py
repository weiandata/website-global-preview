#!/usr/bin/env python3
"""Build a minimal, auditable static-site release directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    "_headers",
    "_redirects",
    "404.html",
    "article.html",
    "index.html",
    "learn.html",
    "llms.txt",
    "llms-full.txt",
    "methods.html",
    "robots.txt",
    "sitemap.xml",
    "support.js",
    "tools.html",
)
ASSET_SUFFIXES = {
    ".avif",
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".png",
    ".svg",
    ".webp",
    ".woff2",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy only public website files into a clean release directory."
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="New directory to create (must not already exist)",
    )
    return parser.parse_args()


def public_files() -> list[Path]:
    files = [ROOT / relative for relative in ROOT_FILES]
    files.extend((ROOT / "articles").glob("*.md"))
    files.extend((ROOT / "articles-en").glob("*.md"))
    files.extend((ROOT / "zh").glob("*.html"))
    files.extend(
        path
        for path in (ROOT / "assets").rglob("*")
        if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES
    )
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> int:
    args = parse_args()
    output = args.output.expanduser().resolve()
    if output.exists():
        print(f"Refusing to replace existing path: {output}", file=sys.stderr)
        return 2
    if output == ROOT or (ROOT in output.parents and output != ROOT / "dist"):
        print("Output must be ./dist or outside the repository root.", file=sys.stderr)
        return 2

    files = public_files()
    if any(path.is_symlink() for path in files):
        print("Release input contains a symbolic link; refusing to continue.", file=sys.stderr)
        return 2

    output.mkdir(parents=True)
    try:
        for source in files:
            relative = source.relative_to(ROOT)
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise

    size = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    print(f"Release created: {output}")
    print(f"Files: {len(files)}; bytes: {size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
