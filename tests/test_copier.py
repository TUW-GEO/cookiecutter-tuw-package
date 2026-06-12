from pathlib import Path


def get_lines(content: str, *, start: int = 0, end: int = -1) -> str:
    return "\n".join(content.splitlines()[start:end])


def test_copier_copies_correct_files(copied_project: Path):
    want: list[str] = [
        ".github/actions/setup/action.yml",
        ".github/workflows/code_quality.yml",
        ".github/workflows/test_coverage.yml",
        ".github/workflows/test_platforms.yml",
        ".gitignore",
        ".gitlab-ci.yml",
        ".pre-commit-config.yaml",
        ".copier-answers.yml",
        "CONTRIBUTING.md",
        "Justfile",
        "LICENSE",
        "README.md",
        "docs/index.ipynb",
        "myst.yml",
        "pyproject.toml",
        "src/my_tuw_project/__init__.py",
        "tests/test_meta.py",
    ]

    for file in want:
        assert (copied_project / file).exists(), f"Missing: {file}"

    for path in copied_project.rglob("*"):
        if path.is_dir():
            continue
        rel = str(path.relative_to(copied_project))
        assert rel in want, f"Unexpected file: {rel}"


def test_init_py_renders_correctly(copied_project: Path):
    got = (copied_project / "src/my_tuw_project/__init__.py").read_text()
    assert 'name = "my_tuw_project"' in got


def test_test_meta_renders_correctly(copied_project: Path):
    got = (copied_project / "tests/test_meta.py").read_text()
    assert "from my_tuw_project import greet" in got


def test_justfile_renders_correctly(copied_project: Path):
    got = (copied_project / "Justfile").read_text()
    assert 'if git rev-parse --git-dir > /dev/null 2>&1; then' in got
    assert 'git init --initial-branch=main' in got


def test_license_renders_correctly(copied_project: Path):
    got = (copied_project / "LICENSE").read_text()
    assert "MIT License" in get_lines(got, end=3)
    assert "Copyright (c)" in get_lines(got, end=3)


def test_pyproject_toml_renders_correctly(copied_project: Path):
    got = (copied_project / "pyproject.toml").read_text()
    want = '[project]\nauthors = [{ name = "TU Wien GEO RS Group", email = "remote.sensing@geo.tuwien.ac.at" }]\nname = "my_tuw_project"\nversion = "0.1.0"\ndescription = "my project description"'
    assert want in got


def test_readme_renders_correctly(copied_project: Path):
    got = (copied_project / "README.md").read_text()
    assert "# my_tuw_project" in got


def test_gitlab_ci_renders_correctly(copied_project: Path):
    got = (copied_project / ".gitlab-ci.yml").read_text()
    assert "my_tuw_project" in got


def test_contributing_renders_correctly(copied_project: Path):
    got = (copied_project / "CONTRIBUTING.md").read_text()
    assert "my_tuw_project" in got


def test_myst_yml_renders_correctly(copied_project: Path):
    got = (copied_project / "myst.yml").read_text()
    assert "my-tuw-project" in got


def test_test_coverage_renders_correctly(copied_project: Path):
    got = (copied_project / ".github/workflows/test_coverage.yml").read_text()
    assert "--cov=my_tuw_project" in got
    assert "GITHUB_TOKEN: ${{ github.token }}" in got


def test_test_platforms_renders_correctly(copied_project: Path):
    got = (copied_project / ".github/workflows/test_platforms.yml").read_text()
    assert "--cov=my_tuw_project" in got
