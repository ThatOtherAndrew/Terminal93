# https://docs.astral.sh/uv/guides/integration/docker/#non-editable-installs

# Install uv
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.14-slim

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Run the application
EXPOSE 8000
CMD ["/app/.venv/bin/terminal93", "--serve", "https://terminal93.fly.dev"]
