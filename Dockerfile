FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir -p /app/viz_image_deobfuscate
COPY pyproject.toml /app 
COPY README.md /app
COPY viz_image_deobfuscate /app/viz_image_deobfuscate

WORKDIR /app
RUN poetry install --no-dev

ENTRYPOINT [ "image-deobfuscate-cli" ]