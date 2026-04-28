import reflex as rx
from urllib.parse import urlparse

from .config import settings

GRAFANA_DASHBOARD_URL = settings.grafana_dashboard_url


def _safe_display_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return "URL configurada"
    return f"{parsed.scheme}://{parsed.netloc}/..."


def grafana_embed() -> rx.Component:
    if not GRAFANA_DASHBOARD_URL:
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("triangle_alert", color="#f59e0b", size=24),
                    rx.heading("Dashboard não configurado", size="5"),
                    align="center",
                    spacing="3",
                ),
                rx.text(
                    "Defina GRAFANA_DASHBOARD_URL ou configure appsettings.toml para exibir o iframe do Grafana.",
                    color_scheme="gray",
                    size="2",
                ),
                spacing="3",
                align="start",
                padding="1.5rem",
            ),
            width="100%",
            max_width="1200px",
            border="1px solid #e5e7eb",
            border_radius="12px",
            background="white",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("chart_no_axes_combined", color="#f46800", size=28),
                rx.heading("Grafana Dashboard", size="5"),
                align="center",
                spacing="3",
            ),
            rx.el.iframe(
                src=GRAFANA_DASHBOARD_URL,
                style={
                    "width": "100%",
                    "height": "720px",
                    "border": "0",
                    "borderRadius": "12px",
                    "background": "#ffffff",
                },
            ),
            rx.text(
                "Se o embed for bloqueado por política do Grafana, use o botão abaixo.",
                color_scheme="gray",
                size="2",
            ),
            rx.link(
                rx.button(
                    rx.icon("external_link", size=16),
                    "Abrir Dashboard no Grafana",
                    color_scheme="orange",
                    size="3",
                ),
                href=GRAFANA_DASHBOARD_URL,
                is_external=True,
            ),
            rx.text(
                _safe_display_url(GRAFANA_DASHBOARD_URL),
                size="1",
                color_scheme="gray",
                font_family="monospace",
                word_break="break-all",
            ),
            spacing="4",
            align="start",
            padding="1.5rem",
        ),
        width="100%",
        max_width="1200px",
        border="1px solid #e5e7eb",
        border_radius="12px",
        background="white",
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Dashboard de Infraestrutura", size="9"),
            rx.text("Gerenciado via Terraform, Docker & GCP", color_scheme="green"),
            grafana_embed(),
            spacing="5",
            width="100%",
            max_width="1240px",
            padding_x="1rem",
        ),
        min_height="100vh",
        width="100%",
        padding_y="2rem",
    )


app = rx.App()
app.add_page(index)