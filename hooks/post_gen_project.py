#!/usr/bin/env python
# ruff: noqa: D100, D101, D103, EXE001
import shutil
from enum import Enum
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd().resolve()


class SupportedCI(Enum):
    GITHUB = "github"
    GITLAB = "gitlab"
    BOTH = "both"


def remove_file(file: str) -> None:
    filepath: Path = PROJECT_DIRECTORY / file
    filepath.unlink()


def remove_dir(directory: str) -> None:
    dir_path: Path = PROJECT_DIRECTORY / directory
    shutil.rmtree(dir_path)


if __name__ == "__main__":
    # Prompted variable values
    approvaltests_root = "{{ cookiecutter.approvaltests_geo_data_root }}"
    approvaltests_ci_vm = "{{ cookiecutter.approvaltests_geo_data_at_ci_vm }}"
    vsc_repo = "{{ cookiecutter.remote_repo_for_ci }}"

    has_pypi = "{{ cookiecutter.external_pypis }}"
    has_docker = {{cookiecutter.package_docker}}  # noqa: F821 # type: ignore[reportUnhashable, reportUndefinedVariable]
    has_code_quality_in_ci = {{cookiecutter.check_code_quality_in_ci}}  # noqa: F821 # type: ignore[reportUnhashable, reportUndefinedVariable]
    has_include_docs = {{cookiecutter.include_docs}}  # noqa: F821 # type: ignore[reportUnhashable, reportUndefinedVariable]
    has_approval = approvaltests_root and (approvaltests_root != approvaltests_ci_vm)

    if not has_approval and not has_pypi and not has_docker:
        remove_dir("ci")
        remove_dir("docker")
    else:
        if not has_approval:
            remove_file("ci/setup-approval-testdata.sh")

        if not has_pypi:
            remove_file("ci/add-pypi-indices.sh")

        if not has_docker:
            remove_file("ci/deploy-docker-image.sh")
            remove_file("ci/deploy-trunk-docker-image.sh")
            remove_dir("docker")

    if not has_include_docs:
        remove_file("zensical.toml")
        remove_dir("docs")

    match vsc_repo:
        case SupportedCI.GITLAB:
            remove_dir(".github")
        case SupportedCI.GITHUB:
            remove_file(".gitlab-ci.yml")
        case SupportedCI.BOTH:
            # Delete none
            pass
        case _:
            err = f"""
            The repository {vsc_repo!r} specified in cookiecutter.vsc_repo,
            is currently not supported.
            Must be one of {[member.value for member in SupportedCI]}.
            """
            raise NotImplementedError(err)

    if not has_code_quality_in_ci:
        remove_file(".github/workflows/code_quality.yml")
        remove_file(".github/actions/setup/action.yml")
