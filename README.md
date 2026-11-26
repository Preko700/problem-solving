# problem-solving

Solutions to algorithmic and logic problems, written in C++17 and Python 3. Every entry has a short write-up (the key idea and its cost) and automated tests.

The goal is not volume: each solution explains *why* the approach works and what it costs.

## Solved problems

<!-- INDEX:START -->
_No problems solved yet._
<!-- INDEX:END -->

## Repository layout

```text
problems/<platform>/<slug>/
  README.md                       write-up with metadata (title, url, difficulty, topics, language)
  solution.py | solution.cpp      the solution
  test_solution.py | test.cpp     tests based on the statement's examples and edge cases
tools/
  new_problem.py                  scaffold a new problem folder
  build_index.py                  regenerate the table above from the write-ups
  tests/                          tests for the tooling itself
templates/                        templates used by the scaffolding script
docs/                             conventions
```

## Workflow

```bash
python tools/new_problem.py --platform cses --slug <slug> --lang cpp \
  --title "<Title>" --url <problem-url> --difficulty medium --topics graphs,dijkstra

# solve it, fill in the write-up and the tests, then:
python tools/build_index.py
```

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest                                        # Python solutions and tooling

cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure    # C++ solutions
```

## Conventions

See [docs/CONVENTIONS.md](docs/CONVENTIONS.md). Personal puzzle inputs (for example from Advent of Code) are never committed; only short examples live in the tests.
