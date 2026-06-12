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
