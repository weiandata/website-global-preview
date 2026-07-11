# Scripts

Use this directory only for small utility scripts that support repository tasks
such as setup, validation, documentation, release preparation, or maintenance.

Business logic must live in the project's language-native source structure, not
in `scripts/`. Each script should have one clear purpose, safe defaults,
documented inputs and outputs, meaningful failures, and a reproducible way to
run it. Do not place credentials, client data, or environment-specific secrets
in scripts.

## Cloudflare Pages build

Build the same clean public directory used by Cloudflare Pages:

```bash
python3 scripts/build_release.py --output dist
```

The builder copies only the ten public HTML files, bilingual article libraries,
runtime assets, discovery files, and the Cloudflare Pages `_headers` policy. It
excludes Git metadata, documentation, developer scripts, editor files, and
credentials. It refuses to overwrite an existing output directory. `dist/` is
ignored by Git and is the only permitted build output inside the repository.

Run `python3 scripts/validate_site.py` before building.
