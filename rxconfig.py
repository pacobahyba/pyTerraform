import os
import reflex as rx

config = rx.Config(
    app_name="pyTerraform",
    api_url=os.environ.get("API_URL", "http://localhost:8000"),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)