from typing import Any, Final
import contextlib
import io
from pathlib import Path

import pytest
from copier import run_copy

DEFAULT_CI_GITHUB_WORKFLOWS: Final = (
    '["Lint_Format", "Test_Coverage", "Test_Platforms"]'
)


def default_answers() -> dict[str, Any]:
    return {
        "project_name": "my-tuw-project",
        "project_description": "my project description",
        "project_url": "",
        "author": "TU Wien GEO RS Group",
        "author_email": "remote.sensing@geo.tuwien.ac.at",
        "ci_github": True,
        "ci_github_workflows": DEFAULT_CI_GITHUB_WORKFLOWS,
        "ci_gitlab": True,
        "use_approvaltests": False,
        "use_external_pypis": False,
        "use_docker": False,
        "include_docs": True,
        "copyright_license": "MIT",
    }


@pytest.fixture(scope="module")
def copied_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_path = tmp_path_factory.mktemp("default")
    cwd = Path(__file__).resolve().parent.parent
    with contextlib.redirect_stdout(io.StringIO()):
        run_copy(
            src_path=str(cwd),
            dst_path=str(tmp_path),
            unsafe=True,
            data=default_answers(),
            vcs_ref="HEAD",
            defaults=True,
            overwrite=True,
        )
    return tmp_path
