FROM swamydev/geo-python:3.12-slim-bookworm
LABEL author={{cookiecutter.author}}
LABEL author_email={{cookiecutter.author_email}}

RUN mkdir -p /etc/uv && mkdir && /etc/netrc
ENV NETRC=/etc/netrc
ENV PATH=/home/cgls/.local/bin:$PATH
COPY --chown=cgls ./ ./src
RUN --mount=type=secret,id=pypi,uid=84242,target=/etc/uv/uv.toml --mount=type=secret,id=netrc,uid=84242,target=/etc/netrc/.netrc \
    cd ./src && uv add gdal=="$(gdal-config --version).*" && uv sync --group trunk

ENTRYPOINT ["{{ cookiecutter.project_name }}"]