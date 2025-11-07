# Cookiecutter Package for TU Wien

Defines a basic project structure for TU Wien python projects. Utilises the [cookiecutter](https://github.com/cookiecutter/cookiecutter) project to efficiently generate project skeletons, keeping a common format.

## Installation

Install cookiecutter in your favourite python environment:

```bash
pip install cookiecutter
# or use uvx to install and run it at once
```

You can also install source, see the [official installation documentation](https://cookiecutter.readthedocs.io/en/2.1.1/installation.html) of the cookiecutter project.

## Usage

Now if you want to generate an initial python project skeleton in TU Wien style, navigate to the folder which should contain the project root project folder and run this command:

```bash
cookiecutter https://github.com/TUW-GEO/cookiecutter-tuw-package

# or with uv (no pip install necessary)
uvx cookiecutter https://github.com/TUW-GEO/cookiecutter-tuw-package
```

This will prompt with some configuration parameters, e.g., package name, author, etc. for most of which reasonable default values are provided.

Once all parameters have been provided, the skeleton will be generated in the current folder.

## Special Parameters

Some cookiecutter parameters have special behaviour, and depend on their value certain files are generated or not.

### vsc_repo

This currently only supports "gitlab" or "github", and depended on which one you choose, it generates a basic CI test and package pipeline for you, using either gitlab or github services.

### approvaltests_geo_data_root and approvaldata_timestamp

If you want to use the [ApprovalTests.Python.GeoExtensions](https://github.com/TUW-GEO/ApprovalTests.Python.GeoExtensions) you can specify the geo approval test data root and the timestamp of the initial approval data data version. This will generate a `pytest.ini` file with the basic geo approval tests configurations.
