---
applyTo: "**/*.cpp,**/*.hpp"
---
- C++17. Expose `void solve(std::istream&, std::ostream&)`; `main` goes behind `#ifndef NO_MAIN`.
- Compile cleanly with `-Wall -Wextra`. Prefer `std::vector` and the STL over raw arrays.
- Tests in `test.cpp` compare `solve` output against expected strings.
