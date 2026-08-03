# Contributing

Keep mathematical classification separate from visualization code. New predicates must define their domain, state the convention being used, include type hints, and have boundary tests. New sequences should be cross-referenced against a canonical source such as OEIS.

Before opening a pull request, run:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

Rendered media should be added only when it documents a meaningful release. Avoid committing temporary frames, caches, or local previews.
