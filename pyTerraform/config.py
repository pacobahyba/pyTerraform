from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import tomllib


@dataclass(frozen=True)
class Settings:
    grafana_dashboard_url: str


def _workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_file_url() -> str:
    config_path = _workspace_root() / "appsettings.toml"
    if not config_path.exists():
        return ""

    with config_path.open("rb") as f:
        data = tomllib.load(f)

    grafana = data.get("grafana", {})
    return str(grafana.get("dashboard_url", "")).strip()


def load_settings() -> Settings:
    env_url = os.environ.get("GRAFANA_DASHBOARD_URL", "").strip()
    file_url = _read_file_url()

    # Environment variable takes precedence over appsettings.toml.
    grafana_dashboard_url = env_url or file_url
    return Settings(grafana_dashboard_url=grafana_dashboard_url)


settings = load_settings()
