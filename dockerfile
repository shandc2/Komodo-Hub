FROM --platform=$BUILDPLATFORM python:alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn"]
CMD ["--bind","0.0.0.0:8000","main:app", "--timeout","120", "--access-logfile", "-", "--error-logfile", "-","--log-level","info"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

COPY --from=gloursdocker/docker / /