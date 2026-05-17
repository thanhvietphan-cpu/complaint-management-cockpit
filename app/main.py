from pathlib import Path
import sys

# Projektordner zum Python-Suchpfad hinzufügen
# Dadurch funktionieren Imports wie "from app.database import ..."
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from nicegui import ui

from app.database import create_tables
from app.pages.complaint_form import show_complaint_form
from app.pages.complaints_list import show_complaints_list
from app.pages.dashboard import show_dashboard


# Datenbanktabellen beim Start der Anwendung erstellen
create_tables()


def create_navigation() -> None:
    """
    Erstellt die Hauptnavigation der Anwendung.
    """
    with ui.header().classes("items-center justify-between"):
        ui.label("Complaint Management Cockpit").classes("text-h5")

        with ui.row().classes("gap-2"):
            ui.button("Dashboard", on_click=lambda: ui.navigate.to("/"))
            ui.button("Reklamationen", on_click=lambda: ui.navigate.to("/complaints"))
            ui.button("Neue Reklamation", on_click=lambda: ui.navigate.to("/complaints/new"))


@ui.page("/")
def dashboard_page() -> None:
    create_navigation()
    show_dashboard()


@ui.page("/complaints")
def complaints_page() -> None:
    create_navigation()
    show_complaints_list()


@ui.page("/complaints/new")
def new_complaint_page() -> None:
    create_navigation()
    show_complaint_form()


ui.run(title="Complaint Management Cockpit", reload=False)