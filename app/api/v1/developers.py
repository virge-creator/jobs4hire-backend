import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.developer import Developer
from app.schemas.developer import DeveloperCreate, DeveloperRead, DeveloperList, DeveloperUpdate

router = APIRouter(prefix="/developers", tags=["developers"])


@router.get("/", response_model=list[DeveloperList])
async def list_developers(
    skill: str | None = None,
    seniority: str | None = None,
    availability: str | None = None,
    remote_preference: str | None = None,
    location: str | None = None,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Developer)

    if skill:
        query = query.where(Developer.skills.has_key(skill))  # noqa: W601
    if seniority:
        query = query.where(Developer.seniority == seniority)
    if availability:
        query = query.where(Developer.availability == availability)
    if remote_preference:
        query = query.where(Developer.remote_preference == remote_preference)
    if location:
        query = query.where(Developer.location.ilike(f"%{location}%"))

    query = query.order_by(Developer.last_active_at.desc().nullslast()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{developer_id}", response_model=DeveloperRead)
async def get_developer(developer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Developer).where(Developer.id == developer_id))
    dev = result.scalar_one_or_none()
    if not dev:
        raise HTTPException(status_code=404, detail="Developer not found")
    return dev


@router.post("/", response_model=DeveloperRead, status_code=201)
async def create_developer(data: DeveloperCreate, db: AsyncSession = Depends(get_db)):
    dev = Developer(**data.model_dump())
    db.add(dev)
    await db.commit()
    await db.refresh(dev)
    return dev


@router.patch("/{developer_id}", response_model=DeveloperRead)
async def update_developer(developer_id: uuid.UUID, data: DeveloperUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Developer).where(Developer.id == developer_id))
    dev = result.scalar_one_or_none()
    if not dev:
        raise HTTPException(status_code=404, detail="Developer not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dev, field, value)

    await db.commit()
    await db.refresh(dev)
    return dev
