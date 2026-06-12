# Copier Package for TU Wien

This template (aka copier) sets up a structure for you to write a python package for TU Wien projects.
It comes filled with a bunch of modern features from the python ecosystem.

## :battery: All Batteries included

- :wrench: CI pipelines for `Github Actions` and `Gitlab`
- :scroll: Documentation from [MyST]
- :zap: Fast environment and project management with [uv]
- :musical_note: Task orchestration with [Just]
- :black_nib: Preconfigured Licenses to choose from
- :straight_ruler: Testing setup with `pytest`
- :fishing_pole_and_fish: Pre-commit Hooks
- :mag: Code Quality Assurance with [ruff] and [ty]

## Usage

> [!NOTE]
> This copier template tries to adhere to the [Python Developer Tooling Handbook](https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/)

To initialize a new repository with this `copier` template run the following command:

```bash
# if you have copier installed
copier copy https://github.com/TUW-GEO/cookiecutter-tuw-package <destination>

# or if you are using uv
uvx copier copy https://github.com/TUW-GEO/cookiecutter-tuw-package <destination>
```

You will be prompted and then your repo will be setup.

## Updating

One advantage of `copier` over `cookiecutter` is the ability to pull in template updates into an existing project:

```bash
copier update
```

Run this inside your generated project to apply changes from the template.

## Approvaltests

If you want to use the [ApprovalTests.Python.GeoExtensions] you can specify the `geo approval test data root` and the `timestamp` of the initial approval data data version.
This will add `pytest.ini_options` in the `pyproject.toml` file with the basic geo approval tests configurations.

[Just]: https://github.com/casey/just
[MyST]: https://mystmd.org/
[ApprovalTests.Python.GeoExtensions]: https://github.com/TUW-GEO/ApprovalTests.Python.GeoExtensions
[uv]: https://docs.astral.sh/uv/
[ruff]: https://docs.astral.sh/ruff/
[ty]: https://docs.astral.sh/ty/
