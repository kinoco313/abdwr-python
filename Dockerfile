FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV MARIMO_SKIP_UPDATE_CHECK=1

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

EXPOSE 2718

CMD ["uv", "run", "marimo", "edit", "--host", "0.0.0.0", "--port", "2718", "--no-token"]
