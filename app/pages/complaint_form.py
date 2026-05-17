from datetime import date

from nicegui import ui

from app.services.complaint_service import create_complaint


def show_complaint_form() -> None:
    """
    Formular zur Anlage eines neuen Reklamationsfalls.

    Sprint-1-Ziel:
    - Pflichtfelder erfassen
    - Pflichtfelder prüfen
    - Reklamationsfall in SQLite speichern
    - nach erfolgreichem Speichern zur Übersicht navigieren
    """

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Neue Reklamation anlegen").classes("text-h4")

        ui.label(
            "Pflichtfelder sind erforderlich, damit der Reklamationsfall gespeichert werden kann."
        ).classes("text-subtitle1 text-grey-7")

        with ui.card().classes("w-full"):
            ui.label("Pflichtangaben").classes("text-h6")

            with ui.grid(columns=2).classes("w-full gap-4"):
                internal_part_number = ui.input(
                    "Teilenummer intern *"
                ).props("outlined").classes("w-full")

                customer = ui.input(
                    "Kunde *"
                ).props("outlined").classes("w-full")

                customer_complaint_id = ui.input(
                    "Kunden-Reklamations-ID *"
                ).props("outlined").classes("w-full")

                defect_pattern = ui.input(
                    "Fehlerbild *"
                ).props("outlined").classes("w-full")

                repeat_defect = ui.select(
                    label="Wiederholfehler *",
                    options=["Nein", "Ja"],
                     value="Nein",
                ).props("outlined").classes("w-full")

                quality_responsible = ui.input(
                    "Verantwortlicher Qualität *"
                ).props("outlined").classes("w-full")

                production_responsible = ui.input(
                    "Verantwortlicher Produktion *"
                ).props("outlined").classes("w-full")

                complaint_date = ui.input(
                    "Reklamationsdatum *",
                    value=date.today().isoformat(),
                ).props("outlined type=date").classes("w-full")

        with ui.card().classes("w-full"):
            ui.label("Weitere Angaben").classes("text-h6")

            with ui.grid(columns=2).classes("w-full gap-4"):
                customer_part_number = ui.input(
                    "Teilenummer Kunde"
                ).props("outlined").classes("w-full")

                product = ui.input(
                    "Produkt / Bauteil"
                ).props("outlined").classes("w-full")

                priority = ui.select(
                    label="Priorität",
                    options=["Niedrig", "Normal", "Hoch", "Kritisch"],
                    value="Normal",
                ).props("outlined").classes("w-full")

                status = ui.select(
                    label="Status",
                    options=["Neu", "In Bearbeitung", "Abgeschlossen"],
                    value="Neu",
                ).props("outlined").classes("w-full")

                received_date = ui.input(
                    "Eingangsdatum",
                    value=date.today().isoformat(),
                ).props("outlined type=date").classes("w-full")

                closed_date = ui.input(
                    "Abschlussdatum"
                ).props("outlined type=date").classes("w-full")

            defect_description = ui.textarea(
                "Fehlerbeschreibung"
            ).props("outlined").classes("w-full")

            remarks = ui.textarea(
                "Bemerkungen"
            ).props("outlined").classes("w-full")

        def validate_required_fields() -> bool:
            """
            Prüft die Pflichtfelder aus dem Lastenheft.
            """

            required_fields = {
                "Teilenummer intern": internal_part_number.value,
                "Kunde": customer.value,
                "Kunden-Reklamations-ID": customer_complaint_id.value,
                "Fehlerbild": defect_pattern.value,
                "Verantwortlicher Qualität": quality_responsible.value,
                "Verantwortlicher Produktion": production_responsible.value,
                "Reklamationsdatum": complaint_date.value,
            }

            missing_fields = [
                field_name
                for field_name, field_value in required_fields.items()
                if field_value is None or str(field_value).strip() == ""
            ]

            if missing_fields:
                ui.notify(
                    "Bitte folgende Pflichtfelder ausfüllen: "
                    + ", ".join(missing_fields),
                    type="negative",
                )
                return False

            return True

        def parse_optional_date(value: str | None):
            """
            Wandelt ein Datumsfeld in ein Python-date-Objekt um.
            Leere optionale Datumsfelder bleiben None.
            """

            if value is None or str(value).strip() == "":
                return None

            return date.fromisoformat(value)

        def save_complaint() -> None:
            """
            Speichert die neue Reklamation.
            """

            if not validate_required_fields():
                return

            try:
                data = {
                    "internal_part_number": internal_part_number.value.strip(),
                    "customer": customer.value.strip(),
                    "customer_complaint_id": customer_complaint_id.value.strip(),
                    "defect_pattern": defect_pattern.value.strip(),
                    "repeat_defect": True if repeat_defect.value == "Ja" else False,
                    "quality_responsible": quality_responsible.value.strip(),
                    "production_responsible": production_responsible.value.strip(),
                    "complaint_date": date.fromisoformat(complaint_date.value),
                    "customer_part_number": customer_part_number.value.strip()
                    if customer_part_number.value
                    else None,
                    "product": product.value.strip() if product.value else None,
                    "defect_description": defect_description.value.strip()
                    if defect_description.value
                    else None,
                    "priority": priority.value,
                    "status": status.value,
                    "received_date": parse_optional_date(received_date.value),
                    "closed_date": parse_optional_date(closed_date.value),
                    "remarks": remarks.value.strip() if remarks.value else None,
                }

                complaint = create_complaint(data)

                ui.notify(
                    f"Reklamation {complaint.complaint_number} wurde gespeichert.",
                    type="positive",
                )

                ui.navigate.to("/complaints")

            except ValueError:
                ui.notify(
                    "Mindestens ein Datumsfeld hat ein ungültiges Format.",
                    type="negative",
                )

            except Exception as error:
                ui.notify(
                    f"Fehler beim Speichern der Reklamation: {error}",
                    type="negative",
                )

        with ui.row().classes("gap-2"):
            ui.button(
                "Speichern",
                on_click=save_complaint,
            ).props("color=primary")

            ui.button(
                "Abbrechen",
                on_click=lambda: ui.navigate.to("/complaints"),
            ).props("outline")