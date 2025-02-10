#!/bin/bash

TOKEN=$1

if [ -f ~/.config/uv/uv.toml ]; then
	echo "uv.toml already exists, you've to add python indices manually."
else
	echo "creating uv.toml..."
	mkdir -p ~/.config/uv
	cat <<- EOF > ~/.config/uv/uv.toml
{%- for pypi_id in cookiecutter.external_pypis.split(',') %}
	[[index]]
	url = "https://gitlab-ci-token:${TOKEN}@git.eodc.eu/api/v4/groups/{{ pypi_id }}/-/packages/pypi/simple/"
{%- endfor %}
	EOF
fi

if [ -f ~/.netrc ]; then
	echo ".netrc already exists, you've to add login credentials manually."
else
	echo "creating .netrc..."
	mkdir -p ~/.config/uv
	cat <<- EOF > ~/.netrc
	machine git.eodc.eu login gitlab-ci-token password ${TOKEN}
	EOF
fi
