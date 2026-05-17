from nicegui import ui

from app.services.complaint_service import get_all_complaints


def show_complaints_list() -> None:
    """
    Zeigt eine Übersicht aller Reklamationsfälle.

    Sprint-1-Ziel:
    - gespeicherte Reklamationen anzeigen
    - zentrale Reklamationsübersicht bereitstellen
    - Basis für spätere Filter und Detailansicht schaffen
    """

    complaints = get_all_complaints()

    rows = [
        {
            "complaint_number": complaint.complaint_number,
            "customer": complaint.customer,
            "internal_part_number": complaint.internal_part_number,
            "customer_complaint_id": complaint.customer_complaint_id,
            "defect_pattern": complaint.defect_pattern,
            "status": complaint.status,
            "priority": complaint.priority,
            "complaint_date": complaint.complaint_date.strftime("%d.%m.%Y"),
            "quality_responsible": complaint.quality_responsible,
            "production_responsible": complaint.production_responsible,
        }
        for complaint in complaints
    ]

    columns = [
        {
            "name": "complaint_number",
            "label": "Reklamationsnummer",
            "field": "complaint_number",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "customer",
            "label": "Kunde",
            "field": "customer",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "internal_part_number",
            "label": "Teilenummer intern",
            "field": "internal_part_number",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "customer_complaint_id",
            "label": "Kunden-Reklamations-ID",
            "field": "customer_complaint_id",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "defect_pattern",
            "label": "Fehlerbild",
            "field": "defect_pattern",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "status",
            "label": "Status",
            "field": "status",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "priority",
            "label": "Priorität",
            "field": "priority",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "complaint_date",
            "label": "Reklamationsdatum",
            "field": "complaint_date",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "quality_responsible",
            "label": "Verantwortlicher Qualität",
            "field": "quality_responsible",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "production_responsible",
            "label": "Verantwortlicher Produktion",
            "field": "production_responsible",
            "align": "left",
            "sortable": True,
        },
    ]

    with ui.column().classes("w-full p-6 gap-4"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Reklamationsübersicht").classes("text-h4")
            ui.button(
                "Neue Reklamation anlegen",
                on_click=lambda: ui.navigate.to("/complaints/new"),
            ).props("color=primary")

        ui.label(
            "Sprint 1: Übersicht aller gespeicherten Reklamationsfälle."
        ).classes("text-subtitle1 text-grey-7")

        if not rows:
            with ui.card().classes("w-full"):
                ui.label("Noch keine Reklamationen vorhanden.").classes("text-h6")
                ui.label(
                    "Lege zuerst eine neue Reklamation an."
                ).classes("text-grey-7")
                ui.button(
                    "Neue Reklamation anlegen",
                    on_click=lambda: ui.navigate.to("/complaints/new"),
                ).props("color=primary")
        else:
            ui.table(
                columns=columns,
                rows=rows,
                row_key="complaint_number",
                pagination=10,
            ).classes("w-full")