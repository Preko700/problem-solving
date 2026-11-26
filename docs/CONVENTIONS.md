# Conventions

## Layout

- One folder per problem: `problems/<platform>/<slug>/`.
- `platform` and `slug` are lowercase kebab-case (`cses`, `codeforces`, `adventofcode`, ...).
- Advent of Code entries use the year and day as the slug, for example `problems/adventofcode/2026-day-01/`.

## Write-up (`README.md` in each problem folder)

The file starts with front matter that the index generator reads:

```text
---
title: ...
platform: ...
url: ...
difficulty: easy | medium | hard
topics: [graphs, dijkstra]
language: python | cpp
date: YYYY-MM-DD
---
```

Then three sections: **Idea**, **Complexity**, **Notes**.

- Link to the problem instead of copying its statement.
- If an editorial, a hint or someone else's explanation helped, say so in **Notes**. A write-up that is honest about its sources is more convincing than a perfect-looking one.

## Tests

- Python: `test_solution.py` loads the sibling `solution.py` through the `load_solution` fixture.
- C++: `test.cpp` includes the sibling `solution.cpp` (with `NO_MAIN` defined) and checks `solve(in, out)` against expected output.
- Cover the statement's examples plus at least one edge case of your own (empty input, a single element, maximum size).
- Remove the `skip` marker from the generated test stub once the cases are filled in.

## What is never committed

- Personal puzzle inputs (`input*.txt`, `inputs/`).
- Copied problem statements.
- Other people's solutions.

## Commits

Keep commits small and in a logical order: for example the solution, then its tests, then the write-up and index update.
