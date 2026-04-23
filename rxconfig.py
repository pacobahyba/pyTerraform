import reflex as rx

config = rx.Config(
    app_name="pyTerraform",
    api_url="https://py-terraform-service-oggamy5kpq-uc.a.run.app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)