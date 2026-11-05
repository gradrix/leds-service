# ---- UI bundle (built once here so the Pi never runs Node) ----
FROM node:22-bookworm-slim AS ui
WORKDIR /ui
COPY ./ui/package.json ./ui/package-lock.json ./
RUN npm ci
COPY ./ui .
RUN npm test && npm run build

# ---- Flask API + static UI ----
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./web_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./gpio_api ./gpio_api
COPY ./web_api .
COPY --from=ui /ui/build ./frontend_build
ENV GPIO_SERVICE_ADDRESS=gpio:9000
EXPOSE 80
# One process, many threads: every live viewer holds a thread for as long as it watches.
# Keep-alive outlasts the 120 s idle timeout of Caddy in front, so a POST never meets a connection closing under it.
CMD ["gunicorn", "-b", "0.0.0.0:80", "--worker-class", "gthread", "--workers", "1", "--threads", "12", "--keep-alive", "130", "--graceful-timeout", "3", "app:app"]
