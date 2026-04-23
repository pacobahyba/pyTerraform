import reflex as rx

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Dashboard de Infraestrutura", size="9"),
            rx.text("Gerenciado via Terraform, Docker & GCP", color_scheme="green"),
            rx.button(
                "Verificar Status", 
                on_click=rx.window_alert("Conectado ao ambiente Python 3.13!"),
                color_scheme="blue",
            ),
            spacing="5",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index)