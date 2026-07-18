FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /workspace

RUN groupadd -g 10003 gateway-group && \
    useradd -u 10003 -g gateway-group -s /bin/bash -m gateway-user

COPY --from=builder /root/.local /home/gateway-user/.local
COPY config.yaml .
COPY src/ ./src/

RUN mkdir -p reports logs && chown -R gateway-user:gateway-group /workspace
USER 10003

ENV PATH=/home/gateway-user/.local/bin:$PATH
ENV PYTHONPATH=/workspace/src

EXPOSE 8080
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]