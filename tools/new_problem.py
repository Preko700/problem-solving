#!/usr/bin/env python3
"""Scaffold a new problem folder from the templates."""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DIFFICULTIES = ("easy", "medium", "hard")
# language -> (solution template, test template, solution file, test file)
LANGUAGES = {
    "python": ("solution.py.tmpl", "test_solution.py.tmpl", "solution.py", "test_solution.py"),
    "cpp": ("solution.cpp.tmpl", "test.cpp.tmpl", "solution.cpp", "test.cpp"),
}


def render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def _write(path: pathlib.Path, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def create_problem(
    *,
    problems_dir: pathlib.Path,
    templates_dir: pathlib.Path,
    platform: str,
    slug: str,
    language: str,
    title: str,
    url: str,
    difficulty: str,
    topics: list[str],
    date: str,
) -> pathlib.Path:
    for label, value in (("platform", platform), ("slug", slug)):
        if not SLUG_RE.match(value):
            raise ValueError(f"{label} must be lowercase kebab-case, got {value!r}")
    if language not in LANGUAGES:
        raise ValueError(f"language must be one of {sorted(LANGUAGES)}, got {language!r}")
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"difficulty must be one of {DIFFICULTIES}, got {difficulty!r}")

    target = problems_dir / platform / slug
    if target.exists():
        raise FileExistsError(f"{target} already exists")

    values = {
        "title": title,
        "platform": platform,
        "url": url,
        "difficulty": difficulty,
        "topics": ", ".join(topics),
        "language": language,
        "date": date,
    }
    solution_tmpl, test_tmpl, solution_name, test_name = LANGUAGES[language]
    files = {
        "README.md": "README.md.tmpl",
        solution_name: solution_tmpl,
        test_name: test_tmpl,
    }

    target.mkdir(parents=True)
    for out_name, tmpl_name in files.items():
        template = (templates_dir / tmpl_name).read_text(encoding="utf-8")
        _write(target / out_name, render(template, values))
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, help="e.g. cses, codeforces, adventofcode")
    parser.add_argument("--slug", required=True, help="kebab-case folder name")
    parser.add_argument("--lang", required=True, choices=sorted(LANGUAGES))
    parser.add_argument("--title", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--difficulty", required=True, choices=DIFFICULTIES)
    parser.add_argument("--topics", default="", help="comma-separated, e.g. graphs,dijkstra")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args(argv)

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    try:
        target = create_problem(
            problems_dir=ROOT / "problems",
            templates_dir=ROOT / "templates",
            platform=args.platform,
            slug=args.slug,
            language=args.lang,
            title=args.title,
            url=args.url,
            difficulty=args.difficulty,
            topics=topics,
            date=args.date,
        )
    except (ValueError, FileExistsError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Created {target.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
