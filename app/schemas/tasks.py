from pydantic import BaseModel
from uuid import UUID
from app.constants.constants import IncidentStatus, IncidentSource
from datetime import datetime


class IncidentCreate(BaseModel):
    description: str
    status: IncidentStatus
    source: IncidentSource


class IncidentBase(IncidentCreate):
    id: UUID
    created_at: datetime
