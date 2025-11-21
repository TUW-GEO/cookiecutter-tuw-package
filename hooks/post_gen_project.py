#!/usr/bin/env python
# ruff: noqa: D100, D101, D103, EXE001
import shutil
from enum import Enum
from pathlib import Path
from rich import print

PROJECT_DIRECTORY = Path.cwd().resolve()


class SupportedCI(str, Enum):
    GITHUB = "github"
    GITLAB = "gitlab"
    BOTH = "both"


class BoolAnswer(str, Enum):
    YES = "yes"
    NO = "no"


def remove_file(file: str) -> None:
    # NOTE: Either fix flow to make sure files dont get removed after their
    # encapsulating directory has already been removed.
    # Or because I am lazy... just try and catch.
    try:
        filepath: Path = PROJECT_DIRECTORY / file
        filepath.unlink()
    except FileNotFoundError:
        print(f"[yellow]Warning: File not found. {file}")


def remove_dir(directory: str) -> None:
    dir_path: Path = PROJECT_DIRECTORY / directory
    shutil.rmtree(dir_path)


if __name__ == "__main__":
    # Prompted variable values
    approvaltests_root: str = "{{ cookiecutter.approvaltests_geo_data_root }}"
    approvaltests_ci_vm: str = "{{ cookiecutter.approvaltests_geo_data_at_ci_vm }}"
    vsc_repo: str = "{{ cookiecutter.remote_repo_for_ci }}"

    has_pypi: str = "{{ cookiecutter.external_pypis }}"
    has_docker: bool = "{{cookiecutter.package_docker}}" == BoolAnswer.YES.value
    has_code_quality_in_ci: bool = (
        "{{cookiecutter.check_code_quality_in_ci}}" == BoolAnswer.YES.value
    )
    has_include_docs: bool = "{{cookiecutter.include_docs}}" == BoolAnswer.YES.value

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
        remove_file("myst.yml")
        remove_dir("docs")

    match vsc_repo:
        case SupportedCI.GITLAB.value:
            remove_dir(".github")
        case SupportedCI.GITHUB:
            remove_file(".gitlab-ci.yml")
        case SupportedCI.BOTH.value:
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

    print(":rocket: [green bold] Project successfully initialized.")
