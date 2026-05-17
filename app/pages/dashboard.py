from nicegui import ui

from app.services.complaint_service import get_all_complaints


def show_dashboard() -> None:
    """
    Einfache Dashboard-Startseite für Sprint 1.

    In späteren Sprints wird diese Seite erweitert um:
    - offene Reklamationen
    - überfällige Maßnahmen
    - Run Charts
    - 6M-Histogramm
    - Maßnahmentracking
    """

    complaints = get_all_complaints()

    total_complaints = len(complaints)
    open_complaints = len(
        [
            complaint
            for complaint in complaints
            if complaint.status in ["Neu", "In Bearbeitung"]
        ]
    )
    closed_complaints = len(
        [
            complaint
            for complaint in complaints
            if complaint.status == "Abgeschlossen"
        ]
    )

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Dashboard").classes("text-h4")

        ui.label(
            "Sprint 1: Erste Übersicht über Reklamationsfälle."
        ).classes("text-subtitle1 text-grey-7")

        with ui.row().classes("gap-4"):
            with ui.card().classes("w-64"):
                ui.label("Reklamationen gesamt").classes("text-subtitle2")
                ui.label(str(total_complaints)).classes("text-h3")

            with ui.card().classes("w-64"):
                ui.label("Offene Reklamationen").classes("text-subtitle2")
                ui.label(str(open_complaints)).classes("text-h3")

            with ui.card().classes("w-64"):
                ui.label("Abgeschlossene Reklamationen").classes("text-subtitle2")
                ui.label(str(closed_complaints)).classes("text-h3")

        ui.separator()

        ui.label("Nächste MVP-Ausbaustufen").classes("text-h6")

        with ui.card().classes("w-full"):
            ui.markdown(
                """
                - Reklamationsfall anlegen
                - Reklamationsübersicht anzeigen
                - Pflichtfelder prüfen
                - 8D-Struktur D1 bis D8 ergänzen
                - Maßnahmenmanagement ergänzen
                - Qualitätswarnung nach D3 erzeugen
                """
            )