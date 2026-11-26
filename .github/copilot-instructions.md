# Copilot instructions for this repository

This repo holds my solutions to algorithmic and logic problems (Python and C++17), each with tests and a short write-up. Read `docs/CONVENTIONS.md` before changing anything.

## Layout
- One folder per problem: `problems/<platform>/<slug>/` (lowercase kebab-case).
- Files per problem: `README.md` (front matter + Idea / Complexity / Notes), `solution.py` or `solution.cpp`, and `test_solution.py` or `test.cpp`.
- Scaffold new problems with `python tools/new_problem.py`, never by hand.
- The index in the root `README.md` is generated: run `python tools/build_index.py` and never edit between the INDEX markers.

## Commands
- Python tests: `pytest`
- C++ tests: `cmake -S . -B build && cmake --build build && ctest --test-dir build`
- Index check (used by CI): `python tools/build_index.py --check`

## Rules
- Every solution ships with tests: the statement examples plus at least one edge case.
- Never commit personal puzzle inputs, copied problem statements, or other people's solutions.
- Write-ups link to the problem instead of copying it, and state honestly which hints or editorials were used.
- Python: type hints, no external dependencies beyond `requirements-dev.txt`.
- C++: C++17, no compiler warnings, `solve(in, out)` as the entry point.
- Keep changes small: one logical change per commit, imperative commit messages.
