from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Complaint(Base):
    """
    Datenmodell für einen Reklamationsfall.

    Dieses Modell bildet die Pflichtfelder aus dem Lastenheft ab:
    - interne Teilenummer
    - Kunde
    - Kunden-Reklamations-ID
    - Fehlerbild
    - Wiederholfehler
    - Verantwortlicher Qualität
    - Verantwortlicher Produktion
    - Reklamationsdatum
    """

    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # automatisch erzeugte interne Reklamationsnummer, z. B. RK-2026-0001
    complaint_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # Pflichtfelder laut Lastenheft
    internal_part_number: Mapped[str] = mapped_column(String(100), nullable=False)
    customer: Mapped[str] = mapped_column(String(150), nullable=False)
    customer_complaint_id: Mapped[str] = mapped_column(String(100), nullable=False)
    defect_pattern: Mapped[str] = mapped_column(String(150), nullable=False)
    repeat_defect: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    quality_responsible: Mapped[str] = mapped_column(String(150), nullable=False)
    production_responsible: Mapped[str] = mapped_column(String(150), nullable=False)
    complaint_date: Mapped[date] = mapped_column(Date, nullable=False)

    # weitere sinnvolle Felder für Sprint 1
    customer_part_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product: Mapped[str | None] = mapped_column(String(150), nullable=True)
    defect_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="Normal")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Neu")
    received_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    closed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Historie / Nachvollziehbarkeit
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )