_default:
    @just --list --unsorted

alias t := test

# run tests
test:
    uv run pytest tests/

# render template to a temp dir for manual inspection
render:
    copier copy . /tmp/copier-tuw-render --overwrite --trust --defaults
