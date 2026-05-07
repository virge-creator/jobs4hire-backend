from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Literal

from app.database import get_db
from app.models.developer import Developer
from app.models.job import Job
from app.schemas.developer import DeveloperList
from app.schemas.job import JobList

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(
    q: str = Query(..., min_length=2, description="Search query"),
    type: Literal["developers", "jobs", "all"] = Query("all", description="Search type"),
    skill: str | None = Query(None, description="Filter by skill"),
    location: str | None = Query(None, description="Filter by location"),
    seniority: str | None = Query(None, description="Filter by seniority level"),
    job_type: str | None = Query(None, description="Filter by job type (contract/permanent)"),
    remote_policy: str | None = Query(None, description="Filter by remote policy"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Full-text search across developers and jobs.
    Uses PostgreSQL to_tsvector and to_tsquery for efficient search.
    """
    results = {"developers": [], "jobs": []}

    # Search developers
    if type in ["developers", "all"]:
        query = select(Developer).where(
            or_(
                func.to_tsvector('english', Developer.full_name).op('@@')(func.plainto_tsquery('english', q)),
                func.to_tsvector('english', func.coalesce(Developer.bio, '')).op('@@')(func.plainto_tsquery('english', q)),
                Developer.skills.has_key(q),  # Check if skill exists in JSONB keys
            )
        )

        # Apply filters
        if location:
            query = query.where(Developer.location.ilike(f"%{location}%"))
        if seniority:
            query = query.where(Developer.seniority == seniority)
        if skill:
            # Check if skill exists in skills JSONB
            query = query.where(Developer.skills.has_key(skill))

        query = query.limit(limit)
        result = await db.execute(query)
        developers = result.scalars().all()
        results["developers"] = [DeveloperList.model_validate(dev) for dev in developers]

    # Search jobs
    if type in ["jobs", "all"]:
        query = select(Job).where(
            or_(
                func.to_tsvector('english', Job.title).op('@@')(func.plainto_tsquery('english', q)),
                func.to_tsvector('english', Job.description).op('@@')(func.plainto_tsquery('english', q)),
                Job.required_skills.overlap([q]),  # Array overlap operator
                Job.nice_to_have_skills.overlap([q]),
            )
        )

        # Apply filters
        if location:
            query = query.where(Job.location.ilike(f"%{location}%"))
        if seniority:
            query = query.where(Job.seniority == seniority)
        if job_type:
            query = query.where(Job.job_type == job_type)
        if remote_policy:
            query = query.where(Job.remote_policy == remote_policy)
        if skill:
            query = query.where(
                or_(
                    Job.required_skills.overlap([skill]),
                    Job.nice_to_have_skills.overlap([skill])
                )
            )

        # Only show active jobs
        query = query.where(Job.status == "active")
        query = query.limit(limit)

        result = await db.execute(query)
        jobs = result.scalars().all()
        results["jobs"] = [JobList.model_validate(job) for job in jobs]

    return results
