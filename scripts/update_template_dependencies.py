# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "httpx>=0.28.1",
#     "rich>=15.0.0",
# ]
# ///
from collections.abc import Sequence

import asyncio
import re
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypedDict

import httpx
from rich import print  # noqa: A004

if TYPE_CHECKING:
    from types import CoroutineType


type PkgName = str


class Resolver(Enum):
    PYPI = auto()
    GITHUB = auto()


class DependencyRule(TypedDict):
    file_glob: str
    package: PkgName
    pattern: str
    resolver: Resolver
    replacement: str


UPDATE_RULES: tuple[DependencyRule, ...] = (
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "mystmd",
        "pattern": '\\"mystmd>=([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"mystmd>={version}"',
    },
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "ruff",
        "pattern": '\\"ruff>=([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"ruff>={version}"',
    },
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "ipykernel",
        "pattern": '\\"ipykernel>=([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"ipykernel>={version}"',
    },
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "pytest",
        "pattern": '\\"pytest>=([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"pytest>={version}"',
    },
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "pytest-cov",
        "pattern": '\\"pytest-cov>=([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"pytest-cov>={version}"',
    },
    {
        "file_glob": "**/pyproject.toml.jinja",
        "package": "uv_build",
        "pattern": '\\"uv_build>=([0-9.]*),<[0-9.]*\\"',
        "resolver": Resolver.PYPI,
        "replacement": '"uv_build>={major_minor},<{next_minor}"',
    },
    {
        "file_glob": "**/*/actions/setup/action.yml",
        "package": "astral-sh/uv",
        "pattern": 'version: \\"([0-9]*.[0-9]*.[0-9]*)\\"',
        "resolver": Resolver.GITHUB,
        "replacement": 'version: "{version}"',
    },
)


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    @classmethod
    def parse(cls, text: str) -> Version:  # noqa: D102
        parts = text.lstrip("v").split(".")
        patch_count = 2
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]),
            patch=int(parts[patch_count]) if len(parts) > patch_count else 0,
        )

    def major_minor(self) -> str:  # noqa: D102
        return f"{self.major}.{self.minor}"

    def next_minor(self) -> Version:  # noqa: D102
        return Version(self.major, self.minor + 1, 0)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.major}.{self.minor}.{self.patch}"


def main() -> None:
    rules = UPDATE_RULES
    template_dir = get_project_root() / "template"
    latest_by_package = fetch_latest_versions(rules)
    for rule in rules:
        apply_rule(rule, template_dir, latest_by_package)


def apply_rule(
    rule: DependencyRule,
    template_dir: Path,
    latest_by_package: dict[PkgName, Version | None],
) -> None:
    for file in template_dir.rglob(rule["file_glob"]):
        update_file_if_outdated(rule, file, latest_by_package)


def update_file_if_outdated(
    rule: DependencyRule,
    file: Path,
    latest_by_package: dict[PkgName, Version | None],
) -> None:
    filename = strip_jinja_tags(file.name)

    current = find_current_version(rule["pattern"], file.read_text())
    if current is None:
        print(fmt(f"Pattern not found for '{rule['package']}' in '{filename}'", "warn"))
        return

    latest = latest_by_package.get(rule["package"])
    if latest is None:
        print(fmt(f"No latest version found for '{rule['package']}'", "warn"))
        return

    if current == latest:
        print(fmt(f"'{rule['package']}' already at latest: {latest}", "info"))
        return

    msg = fmt(f"'{rule['package']}' in {filename}: {current} \u2192 {latest}", "update")
    print(msg)

    replacement = rule["replacement"].format(
        version=latest,
        major_minor=latest.major_minor(),
        next_minor=latest.next_minor().major_minor(),
    )
    rewrite_file(file, re.compile(rule["pattern"]), replacement)


def strip_jinja_tags(name: str) -> str:
    return re.sub(r"({%.*?%}|{{.*?}}|{#.*?#})", "", name)


def find_current_version(pattern: str, content: str) -> Version | None:
    matches = re.findall(pattern, content)
    if not matches:
        return None
    if len(matches) > 1:
        print(fmt(f"multiple version matches found: {matches}", "warn"))
    return Version.parse(sorted(matches, reverse=True)[0])


def rewrite_file(file: Path, pattern: re.Pattern[str], replacement: str) -> None:
    file.write_text(pattern.sub(replacement, file.read_text()))


def fetch_latest_versions(
    rules: Sequence[DependencyRule],
) -> dict[PkgName, Version | None]:
    results = asyncio.run(fetch_all_package_versions(rules))
    return dict(results)


async def fetch_all_package_versions(
    rules: Sequence[DependencyRule],
) -> list[tuple[PkgName, Version | None]]:
    async with httpx.AsyncClient() as client:
        tasks: list[CoroutineType[Any, Any, tuple[PkgName, Version | None]]] = [
            fetch_package_version(rule, client) for rule in rules
        ]
        return await asyncio.gather(*tasks)


async def fetch_package_version(
    rule: DependencyRule, client: httpx.AsyncClient
) -> tuple[PkgName, Version | None]:
    match rule["resolver"]:
        case Resolver.PYPI:
            version = await fetch_latest_from_pypi(rule["package"], client)
            return rule["package"], version
        case Resolver.GITHUB:
            version = await fetch_latest_from_github(rule["package"], client)
            return rule["package"], version
        case _:
            return rule.package, None


async def fetch_latest_from_github(
    pkg: PkgName, client: httpx.AsyncClient
) -> Version | None:
    url = f"https://api.github.com/repos/{pkg}/releases/latest"
    resp = await client.get(url, timeout=10)
    if resp.status_code != httpx.codes.OK:
        msg = fmt(f"fetching '{pkg}' from Github (HTTP {resp.status_code})", "error")
        print(msg)
        return None
    version_str = resp.json().get("tag_name", "")
    return Version.parse(version_str) if version_str else None


async def fetch_latest_from_pypi(
    pkg: PkgName, client: httpx.AsyncClient
) -> Version | None:
    resp = await client.get(f"https://pypi.org/pypi/{pkg}/json", timeout=10)
    if resp.status_code != httpx.codes.OK:
        msg = fmt(f"fetching '{pkg}' from PyPI (HTTP {resp.status_code})", "error")
        print(msg)
        return None
    version_str: str | None = resp.json().get("info", {}).get("version")
    return Version.parse(version_str) if version_str else None


class ProjectRootNotFoundError(FileNotFoundError):
    """Raised when no project root marker is found in any parent directory."""


def get_project_root() -> Path:
    marker = ".git"
    cwd = Path.cwd()
    if (cwd / marker).exists():
        return cwd
    for parent in cwd.parents:
        if (parent / marker).exists():
            return parent
    err = f"no '{marker}' found in any parent directories"
    raise ProjectRootNotFoundError(err)


def fmt(msg: str, kind: Literal["error", "warn", "info", "update"] = "info") -> str:
    prefix = {
        "error": "[red bold]error[/red bold]: ",
        "info": "[turquoise2 bold]info[/turquoise2 bold]: ",
        "warn": "[yellow bold]warn[/yellow bold]: ",
        "update": "[green bold]update[/green bold]: ",
    }
    return prefix[kind] + msg


if __name__ == "__main__":
    raise SystemExit(main())
