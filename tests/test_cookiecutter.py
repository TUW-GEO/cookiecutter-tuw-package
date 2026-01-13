from pathlib import Path
from pytest import TempPathFactory
import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_PATH = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def session_tmp_path(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("cookiecutter")


def _get_path(root: Path, file: str) -> Path:
    return root / "destination/my-tuw-project" / file


def _get_filelines(content: str, *, start: int = 0, end: int = -1) -> str:
    """Reduce noise, when test fails, and complete file content would be shown."""
    lines: list[str] = content.splitlines()
    return "\n".join(lines[start:end])


def test_cookicutter_copies_correct_files(
    session_tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    dst: Path = session_tmp_path / "destination"
    project: Path = dst / "my-tuw-project"

    cookiecutter(
        template=str(TEMPLATE_PATH),
        output_dir=str(dst.resolve()),
        default_config=True,
        no_input=True,
    )
    _ = capsys.readouterr()

    wanted_files: list[str] = [
        ".github/actions/setup/action.yml",
        ".github/workflows/code_quality.yml",
        ".github/workflows/test_coverage.yml",
        ".github/workflows/test_platforms.yml",
        ".gitignore",
        ".gitlab-ci.yml",
        ".pre-commit-config.yaml",
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

    for file in wanted_files:
        assert (project / file).exists()

    # Assert no files where not accounted for
    wanted_files_paths: list[Path] = [(project / f) for f in wanted_files]
    for got in project.iterdir():
        if got.is_file():
            assert got in wanted_files_paths


def test_init_py_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "src/my_tuw_project/__init__.py")
    got: str = file.read_text()

    want = 'name = "my_tuw_project"'
    lines = _get_filelines(got, start=5, end=7)
    assert want in lines


def test_test_meta_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "tests/test_meta.py")
    got: str = file.read_text()

    want = "from my_tuw_project import greet"
    lines = _get_filelines(got, end=3)
    assert want in lines


def test_justfile_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "Justfile")
    got: str = file.read_text()

    # {{ PYTHON }} should not be rendered
    want = 'ci PYTHON="3.12":\n    uv run --python={{ PYTHON }} ruff'
    lines = _get_filelines(got, start=45, end=48)
    assert want in lines


def test_license_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "LICENSE")
    got: str = file.read_text()

    want = "MIT License\n\nCopyright (c)"
    lines = _get_filelines(got, end=3)
    assert want in lines


def test_pyproject_toml_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "pyproject.toml")
    got: str = file.read_text()

    want = """[project]
authors = [{ name = "TU Wien GEO RS Group", email = "remote.sensing@geo.tuwien.ac.at" }]
name = "my_tuw_project"
version = "0.1.0"
description = "my project description"\
"""

    lines = _get_filelines(got, end=5)
    assert want in lines


def test_readme_renders_correctly(session_tmp_path: Path):
    file = _get_path(session_tmp_path, "README.md")
    got: str = file.read_text()

    want = "# my_tuw_project"
    lines = _get_filelines(got, end=3)
    assert want in lines
