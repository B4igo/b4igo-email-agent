"""Runtime configuration for the admin panel."""

import os
import secrets

ADMIN_PASSWORD = os.environ.get("B4IGO_ADMIN_PANEL_PASSWORD", "admin")
SESSION_SECRET = os.environ.get("B4IGO_ADMIN_PANEL_SECRET") or secrets.token_hex(32)
SESSION_COOKIE = "b4igo_admin_session"
SESSION_TTL_SECONDS = 8 * 60 * 60

BACKEND_URL = os.environ.get("B4IGO_BACKEND_URL", "http://backend:5000").rstrip("/")
BACKEND_ADMIN_TOKEN = os.environ.get("B4IGO_ADMIN_TOKEN", "")
AI_SERVICE_URL = os.environ.get(
    "B4IGO_AI_SERVICE_URL", "http://ai-service:5300"
).rstrip("/")

MAIL_HOST = os.environ.get("MAIL_HOST", "mailserver")
MAIL_DOMAIN = os.environ.get("MAIL_DOMAIN", "test.local")
MAIL_SMTP_PORT = int(os.environ.get("MAIL_SMTP_PORT", "25"))

DEFAULT_CONTAINERS = [
    "mailserver",
    "webmail",
    "b4igo-account-manager",
    "b4igo-redis",
    "b4igo-scheduler",
    "ai-service",
    "b4igo-backend",
    "b4igo-frontend",
]
_env_containers = os.environ.get("B4IGO_PANEL_CONTAINERS", "")
PANEL_CONTAINERS = (
    [c.strip() for c in _env_containers.split(",") if c.strip()]
    if _env_containers
    else DEFAULT_CONTAINERS
)

PIPELINE_STAGE_CONTAINERS = {
    "mail": "mailserver",
    "scheduler": "b4igo-scheduler",
    "ai": "ai-service",
    "backend": "b4igo-backend",
}

SELF_CONTAINER_NAME = os.environ.get("HOSTNAME", "")
