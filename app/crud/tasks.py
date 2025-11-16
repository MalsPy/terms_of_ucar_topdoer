from sqlalchemy import select, update
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Base, Incident
from app.core.db import engine
from app.schemas.tasks import IncidentCreate


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class Incidents:
    @staticmethod
    async def get_all_incidents(
        session: AsyncSession, status: str | None = None
    ) -> list[Incident]:
        query = select(Incident)
        if status:
            query = query.where(Incident.status == status)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_incident(
        session: AsyncSession, incident_data: IncidentCreate
    ) -> Incident:
        incident = Incident(id=uuid4(), **incident_data.model_dump())
        session.add(incident)
        await session.commit()
        await session.refresh(incident)
        return incident

    @staticmethod
    async def get_incident_by_id(
        session: AsyncSession, incident_id: UUID
    ) -> Incident | None:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_incident_fully(
        session: AsyncSession, incident_id: UUID, new_data: IncidentCreate
    ) -> Incident | None:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()
        if not incident:
            return None
        for key, value in new_data.model_dump().items():
            setattr(incident, key, value)
        await session.commit()
        await session.refresh(incident)
        return incident

    @staticmethod
    async def update_incident_status(
        session: AsyncSession, incident_id: UUID, new_status: str
    ) -> Incident | None:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()
        if not incident:
            return None
        incident.status = new_status
        await session.commit()
        await session.refresh(incident)
        return incident

    @staticmethod
    async def update_incident_partially(
        session: AsyncSession, incident_id: UUID, update_data: dict
    ) -> Incident | None:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()
        if not incident:
            return None
        for key, value in update_data.items():
            if hasattr(incident, key):
                setattr(incident, key, value)
        await session.commit()
        await session.refresh(incident)
        return incident

    @staticmethod
    async def delete_incident_by_id(session: AsyncSession, incident_id: UUID) -> bool:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()
        if not incident:
            return False
        await session.delete(incident)
        await session.commit()
        return True
