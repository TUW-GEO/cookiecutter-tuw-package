_default:
    @just --list --unsorted

alias t := test

# run tests
test *args:
    uv run pytest tests/ {{ args }}

# update the template dependencies
update:
    (cd template && uvx prek autoupdate)
    uv run scripts/update_template_dependencies.py

# render template to a temp dir for manual inspection
render:
    copier copy . ./rendered --overwrite --trust --defaults -r HEAD \
        --data project_name=my-tuw-project \
        --data project_description="my project description" \
        --data project_url="https://github.com/TUW-GEO/my-tuw-project" \
        --data author="TU Wien GEO RS Group" \
        --data author_email=remote.sensing@geo.tuwien.ac.at \
        --data ci_github=true \
        --data 'ci_github_workflows=["Lint_Format", "Test_Coverage", "Test_Platforms"]' \
        --data ci_gitlab=true \
        --data use_approvaltests=true \
        --data use_external_pypis=true \
        --data use_docker=true \
        --data include_docs=true \
        --data copyright_license=MIT

# run the formatter, linter, typechecker and the tests
ci py="3.14":
    uv run --python={{ py }} ruff format .
    uv run --python={{ py }} ruff check . --fix
    uv run --python={{ py }} ty check .
    uv run --python={{ py }} pytest tests/

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

_set_version target:
    case "{{ target }}" in \
        [0-9]*.[0-9]*.[0-9]*) \
            uv version {{ target }} ;; \
        *) \
            uv version --bump {{ target }} ;; \
    esac
    uv lock

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock
    git commit -m "chore(release): bump version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release [target:<major|minor|patch|...> or semver]
release target: ci
    @just _ensure_clean
    @just _set_version {{ target }}
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
