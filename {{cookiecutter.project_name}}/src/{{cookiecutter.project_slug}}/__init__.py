"""{{ cookiecutter.project_slug }}: Package to do ..."""

from importlib.metadata import version

__version__ = version(__name__)

name = "{{ cookiecutter.project_slug }}"


def greet() -> str:
    return "Hello from {{ cookiecutter.project_slug }}"
