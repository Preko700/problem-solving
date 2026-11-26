import importlib.util
import pathlib
import shutil

import pytest

TOOLS = pathlib.Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


new_problem = load("new_problem")
build_index = load("build_index")


def make(problems_dir, **overrides):
    values = dict(
        problems_dir=problems_dir,
        templates_dir=ROOT / "templates",
        platform="cses",
        slug="example-problem",
        language="python",
        title="Example Problem",
        url="https://example.com/problem",
        difficulty="medium",
        topics=["graphs", "dijkstra"],
        date="2026-12-01",
    )
    values.update(overrides)
    return new_problem.create_problem(**values)


def test_creates_python_problem(tmp_path):
    target = make(tmp_path / "problems")
    assert sorted(p.name for p in target.iterdir()) == [
        "README.md",
        "solution.py",
        "test_solution.py",
    ]
    meta = build_index.parse_front_matter((target / "README.md").read_text(encoding="utf-8"))
    assert meta["title"] == "Example Problem"
    assert meta["topics"] == "[graphs, dijkstra]"
    assert meta["language"] == "python"


def test_creates_cpp_problem(tmp_path):
    target = make(tmp_path / "problems", language="cpp")
    assert sorted(p.name for p in target.iterdir()) == ["README.md", "solution.cpp", "test.cpp"]
    assert "NO_MAIN" in (target / "test.cpp").read_text(encoding="utf-8")


@pytest.mark.parametrize("field", ["platform", "slug"])
def test_rejects_bad_names(tmp_path, field):
    with pytest.raises(ValueError):
        make(tmp_path / "problems", **{field: "Not Kebab"})


def test_rejects_existing_folder(tmp_path):
    make(tmp_path / "problems")
    with pytest.raises(FileExistsError):
        make(tmp_path / "problems")


def test_index_is_generated_and_checked(tmp_path):
    shutil.copy(ROOT / "README.md", tmp_path / "README.md")
    problems = tmp_path / "problems"
    make(problems, slug="b-problem", title="B Problem", difficulty="hard", date="2026-12-02")
    make(problems, slug="a-problem", title="A Problem", difficulty="easy", language="cpp")

    assert build_index.update_readme(tmp_path, check=True) == 1
    assert build_index.update_readme(tmp_path) == 0
    text = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "**2 problems** - 1 easy, 0 medium, 1 hard" in text
    assert "[A Problem](problems/cses/a-problem/)" in text
    assert "[B Problem](problems/cses/b-problem/)" in text
    assert build_index.update_readme(tmp_path, check=True) == 0


def test_unclosed_front_matter_is_ignored():
    assert build_index.parse_front_matter("---\ntitle: x\n") == {}
