FROM swamydev/geo-python:3.12-slim-bookworm
LABEL author={{cookiecutter.author}}
LABEL author_email={{cookiecutter.author_email}}

RUN mkdir -p /etc/uv && mkdir && /etc/netrc && mkdir -p /root/.local/bin
ENV NETRC=/etc/netrc
ENV PATH=/root/.local/bin:$PATH
COPY ./ ./src
RUN --mount=type=secret,id=pypi,uid=84242,target=/etc/uv/uv.toml --mount=type=secret,id=netrc,uid=84242,target=/etc/netrc/.netrc \
    cd ./src && make uv

ENTRYPOINT ["./src/.venv/bin/{{ cookiecutter.project_name }}"]