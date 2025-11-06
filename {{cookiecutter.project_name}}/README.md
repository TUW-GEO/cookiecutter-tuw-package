# {{ cookiecutter.project_slug }}

![Static Badge](https://img.shields.io/badge/TU_Wien_GEO-Project-gray?style=flat&labelColor=%23006699&color=gray)


TODO: Add documentation!

## First Steps

After you have just used the `cookiecutter` to create this repo, you might want to follow these steps:

1. Initialize a git repo with `git init` or you could also use `uv init`
2. Install the Pre-Commit Hooks, to identify simple issues before commiting. You can run `just hooks` or use `uvx pre-commit install`
3. Set up a virtual environment. You might want to use `uv add <package>` to add dependencies to your project (no `pip install` necessary)

## Development

> [!TIP]
> This project uses `uv` for package management and development tasks and `Make`and/or `Just` for task automation.
> To install `Just`, follow the instructions in the [Just Docs].
>
> To install `uv`, you can use the following command:
>
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
>
> # For convenience also possible via PyPI
> pip install uv
> ```
>
> or check the [uv Docs]

The Pre-commit Hooks will lint and format your code, aswell as running some checks.
In order to use the Pre-commit hooks, run:

```bash
pip install pre-commit
pre-commit install

# Alternatively via uv tool runner
uvx pre-commit install
```

or use the Justfile to do the same:

```bash
just hooks
```

By default cody quality checks (formatter, linter and type-checker) are inplace, via the `Github Actions` (`GitLab CI/CD` has not been setup), which does the same as the `pre-commit` hooks.

Additionally the same code quality checks can be run manually via:

```bash
just check

# or manually with
uvx ruff check . --fix
uvx ruff format .
uvx ty check
```

> [!IMPORTANT]
> The configuration for the linter, the formatter and the typechecker can be done in the `pyproject.toml` file.
> By default ALL Linting Rules are enabled. If some rule are not desired in the project use the `exclude` field to disregard them.

[Just Docs]: https://github.com/casey/just
[uv Docs]: https://docs.astral.sh/uv/getting-started/installation/
