from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, DateTime, func
from uuid import UUID, uuid4

from app.core.base import Base, str_256
from app.constants.constants import IncidentStatus, IncidentSource


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    description: Mapped[str_256]  # текст/описание
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), nullable=False, default=IncidentStatus.NEW
    )
    source: Mapped[IncidentSource] = mapped_column(Enum(IncidentSource), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    repr_cols = ("id", "status", "source", "created_at")
