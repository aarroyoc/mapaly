# End-2-end Tests

These tests should run with the full application running at localhost:1133 and some example data.

Then:
```
docker build -t mapaly-e2e .
docker run --rm --network host mapaly-e2e
```