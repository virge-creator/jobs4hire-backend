import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobRead, JobList, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


def make_slug(title: str) -> str:
    try:
        return slugify(title)
    except Exception:
        return title.lower().replace(" ", "-")


@router.get("/", response_model=list[JobList])
async def list_jobs(
    skill: str | None = None,
    job_type: str | None = None,
    remote_policy: str | None = None,
    seniority: str | None = None,
    location: str | None = None,
    status: str = "active",
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Job).where(Job.status == status)

    if skill:
        query = query.where(Job.required_skills.any(skill))
    if job_type:
        query = query.where(Job.job_type == job_type)
    if remote_policy:
        query = query.where(Job.remote_policy == remote_policy)
    if seniority:
        query = query.where(Job.seniority == seniority)
    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))

    query = query.order_by(Job.featured.desc(), Job.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # Increment views
    job.views += 1
    await db.commit()
    return job


@router.post("/", response_model=JobRead, status_code=201)
async def create_job(data: JobCreate, company_id: uuid.UUID = Query(...), db: AsyncSession = Depends(get_db)):
    job = Job(
        **data.model_dump(),
        company_id=company_id,
        slug=make_slug(data.title) + "-" + uuid.uuid4().hex[:6],
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.patch("/{job_id}", response_model=JobRead)
async def update_job(job_id: uuid.UUID, data: JobUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    await db.commit()
    await db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=204)
async def close_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = "closed"
    await db.commit()
