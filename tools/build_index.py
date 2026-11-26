#!/usr/bin/env python3
"""Regenerate the problem index in README.md from the problem write-ups."""
from __future__ import annotations

import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"
MARKERS = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
DIFFICULTIES = ("easy", "medium", "hard")


def parse_front_matter(text: str) -> dict[str, str]:
    """Read the simple ``key: value`` block between the leading ``---`` lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        key, sep, value = line.partition(":")
        if sep:
            data[key.strip()] = value.strip()
    return {}  # the block was never closed


def collect_entries(problems_dir: pathlib.Path) -> list[dict[str, str]]:
    entries = []
    for readme in sorted(problems_dir.glob("*/*/README.md")):
        meta = parse_front_matter(readme.read_text(encoding="utf-8"))
        if not meta.get("title") or not meta.get("platform"):
            continue
        meta["path"] = readme.parent.relative_to(problems_dir.parent).as_posix()
        entries.append(meta)
    entries.sort(key=lambda e: (e["platform"], e.get("date", ""), e["title"]))
    return entries


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def render_index(entries: list[dict[str, str]]) -> str:
    if not entries:
        return "_No problems solved yet._"
    counts = {name: 0 for name in DIFFICULTIES}
    for entry in entries:
        if entry.get("difficulty") in counts:
            counts[entry["difficulty"]] += 1
    lines = [
        f"**{len(entries)} problems** - "
        f"{counts['easy']} easy, {counts['medium']} medium, {counts['hard']} hard",
        "",
        "| Problem | Platform | Difficulty | Topics | Language |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        topics = entry.get("topics", "").strip("[]")
        lines.append(
            f"| [{_cell(entry['title'])}]({entry['path']}/) | {_cell(entry['platform'])} "
            f"| {_cell(entry.get('difficulty', ''))} | {_cell(topics)} "
            f"| {_cell(entry.get('language', ''))} |"
        )
    return "\n".join(lines)


def update_readme(root: pathlib.Path, check: bool = False) -> int:
    """Return 0 when the README is current (or was updated), 1 when stale in check mode."""
    readme = root / "README.md"
    old = readme.read_text(encoding="utf-8")
    if START not in old or END not in old:
        print(f"error: {readme} is missing the {START} / {END} markers")
        return 2
    block = f"{START}\n{render_index(collect_entries(root / 'problems'))}\n{END}"
    new = MARKERS.sub(lambda _match: block, old, count=1)
    if new == old:
        return 0
    if check:
        print("README index is out of date; run: python tools/build_index.py")
        return 1
    with open(readme, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(new)
    print("README index updated")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the index is stale")
    args = parser.parse_args(argv)
    return update_readme(ROOT, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
