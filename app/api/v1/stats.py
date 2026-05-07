from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.developer import Developer
from app.models.job import Job
from app.models.company import Company
from app.models.application import Application

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get public platform statistics."""
    
    # Count developers
    dev_result = await db.execute(select(func.count(Developer.id)))
    total_developers = dev_result.scalar()

    # Count active jobs
    job_result = await db.execute(
        select(func.count(Job.id)).where(Job.status == "active")
    )
    total_jobs = job_result.scalar()

    # Count all jobs (for total job postings metric)
    all_jobs_result = await db.execute(select(func.count(Job.id)))
    total_job_postings = all_jobs_result.scalar()

    # Count companies
    company_result = await db.execute(select(func.count(Company.id)))
    total_companies = company_result.scalar()

    # Count applications
    app_result = await db.execute(select(func.count(Application.id)))
    total_applications = app_result.scalar()

    # Count hired applications
    hired_result = await db.execute(
        select(func.count(Application.id)).where(Application.status == "hired")
    )
    successful_hires = hired_result.scalar()

    return {
        "developers": total_developers,
        "active_jobs": total_jobs,
        "total_job_postings": total_job_postings,
        "companies": total_companies,
        "applications": total_applications,
        "successful_hires": successful_hires,
    }
