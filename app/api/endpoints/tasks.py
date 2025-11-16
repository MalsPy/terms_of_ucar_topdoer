from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tasks import IncidentCreate, IncidentBase
from app.crud.tasks import Incidents
from app.api.deps import get_session

router = APIRouter()


@router.get("/incidents", response_model=List[IncidentBase])
async def get_all_incidents(
    status: str | None = None, session: AsyncSession = Depends(get_session)
):
    return await Incidents.get_all_incidents(session, status)


@router.get("/incidents/{incident_id}", response_model=IncidentBase)
async def get_incident_by_id(
    incident_id: UUID, session: AsyncSession = Depends(get_session)
):
    incident = await Incidents.get_incident_by_id(session, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return incident


@router.post("/incidents", response_model=IncidentBase)
async def create_incident(
    incident_data: IncidentCreate, session: AsyncSession = Depends(get_session)
):
    return await Incidents.create_incident(session, incident_data)


@router.put("/incidents/{incident_id}", response_model=IncidentBase)
async def update_incident_fully(
    incident_id: UUID,
    incident_data: IncidentCreate,
    session: AsyncSession = Depends(get_session),
):
    updated_incident = await Incidents.update_incident_fully(
        session, incident_id, incident_data
    )
    if not updated_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return updated_incident


@router.patch("/incidents/{incident_id}", response_model=IncidentBase)
async def update_incident_partially(
    incident_id: UUID, update_data: dict, session: AsyncSession = Depends(get_session)
):
    updated_incident = await Incidents.update_incident_partially(
        session, incident_id, update_data
    )
    if not updated_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return updated_incident


@router.patch("/incidents/{incident_id}/status", response_model=IncidentBase)
async def update_incident_status(
    incident_id: UUID, new_status: str, session: AsyncSession = Depends(get_session)
):
    updated_incident = await Incidents.update_incident_status(
        session, incident_id, new_status
    )
    if not updated_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return updated_incident


@router.delete("/incidents/{incident_id}")
async def delete_incident(
    incident_id: UUID, session: AsyncSession = Depends(get_session)
):
    deleted = await Incidents.delete_incident_by_id(session, incident_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return {"success": True, "message": f"Incident {incident_id} deleted"}
