from datetime import date
from typing import Any

from app.database import get_db_session
from app.models import Complaint


def generate_complaint_number() -> str:
    """
    Erzeugt eine fortlaufende interne Reklamationsnummer.
    Format: RK-JAHR-0001
    Beispiel: RK-2026-0001
    """
    current_year = date.today().year

    db = get_db_session()
    try:
        last_complaint = (
            db.query(Complaint)
            .filter(Complaint.complaint_number.like(f"RK-{current_year}-%"))
            .order_by(Complaint.id.desc())
            .first()
        )

        if last_complaint is None:
            next_number = 1
        else:
            last_number_text = last_complaint.complaint_number.split("-")[-1]
            next_number = int(last_number_text) + 1

        return f"RK-{current_year}-{next_number:04d}"

    finally:
        db.close()


def create_complaint(data: dict[str, Any]) -> Complaint:
    """
    Erstellt einen neuen Reklamationsfall in der Datenbank.
    """

    db = get_db_session()
    try:
        complaint = Complaint(
            complaint_number=generate_complaint_number(),
            internal_part_number=data["internal_part_number"],
            customer=data["customer"],
            customer_complaint_id=data["customer_complaint_id"],
            defect_pattern=data["defect_pattern"],
            repeat_defect=data["repeat_defect"],
            quality_responsible=data["quality_responsible"],
            production_responsible=data["production_responsible"],
            complaint_date=data["complaint_date"],
            customer_part_number=data.get("customer_part_number"),
            product=data.get("product"),
            defect_description=data.get("defect_description"),
            priority=data.get("priority", "Normal"),
            status=data.get("status", "Neu"),
            received_date=data.get("received_date"),
            closed_date=data.get("closed_date"),
            remarks=data.get("remarks"),
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return complaint

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_all_complaints() -> list[Complaint]:
    """
    Lädt alle Reklamationsfälle aus der Datenbank.
    Neueste Einträge stehen oben.
    """

    db = get_db_session()
    try:
        complaints = (
            db.query(Complaint)
            .order_by(Complaint.id.desc())
            .all()
        )
        return complaints

    finally:
        db.close()


def get_complaint_by_id(complaint_id: int) -> Complaint | None:
    """
    Lädt einen einzelnen Reklamationsfall anhand der internen ID.
    """

    db = get_db_session()
    try:
        return (
            db.query(Complaint)
            .filter(Complaint.id == complaint_id)
            .first()
        )

    finally:
        db.close()