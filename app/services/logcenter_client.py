import json
import logging
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from threading import Thread

BRT = timezone(timedelta(hours=-3))
logger = logging.getLogger(__name__)


class LogCenterClient:
    def __init__(self, base_url: str, api_key: str, project_id: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.project_id = project_id

    def log(
        self,
        *,
        level: str,
        status: str,
        message: str,
        data: dict | None = None,
        tags: list[str] | None = None,
    ) -> None:
        payload = {
            "project_id": self.project_id,
            "level": level,
            "status": status,
            "message": message,
            "timestamp": datetime.now(BRT).isoformat(),
            "data": data or {},
            "tags": tags or [],
        }
        Thread(target=self._send, args=(payload,), daemon=True).start()

    def _send(self, payload: dict) -> None:
        try:
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/logs/",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "X_API_Key": self.api_key,
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                logger.debug("LogCenter %s %s", resp.status, payload.get("message"))
        except urllib.error.HTTPError as e:
            body_err = e.read().decode("utf-8", errors="replace")
            logger.error("LogCenter HTTP %s: %s", e.code, body_err)
        except Exception as e:
            logger.error("LogCenter error: %s", e)

    @classmethod
    def from_app(cls, app) -> "LogCenterClient":
        return cls(
            base_url=app.config["LOG_BASE_URL"],
            api_key=app.config["LOG_API_KEY"],
            project_id=app.config["LOG_PROJECT_ID"],
        )
