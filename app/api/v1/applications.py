import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.developer import Developer
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=201)
async def apply_to_job(
    job_id: uuid.UUID,
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Developer applies to a job."""
    # Check if job exists
    job_result = await db.execute(select(Job).where(Job.id == job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if developer exists
    dev_result = await db.execute(select(Developer).where(Developer.id == application.developer_id))
    developer = dev_result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")

    # Check for duplicate application
    existing_result = await db.execute(
        select(Application).where(
            Application.job_id == job_id,
            Application.developer_id == application.developer_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="You have already applied to this job")

    # Create application
    db_application = Application(
        job_id=job_id,
        developer_id=application.developer_id,
        cover_letter=application.cover_letter
    )
    db.add(db_application)

    # Update job application count
    job.application_count += 1

    await db.commit()
    await db.refresh(db_application)
    return db_application


@router.get("/jobs/{job_id}/applications", response_model=list[ApplicationResponse])
async def list_job_applications(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """List all applications for a specific job."""
    # Verify job exists
    job_result = await db.execute(select(Job).where(Job.id == job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get applications
    result = await db.execute(
        select(Application)
        .where(Application.job_id == job_id)
        .order_by(Application.created_at.desc())
    )
    applications = result.scalars().all()
    return applications


@router.get("/developers/{dev_id}/applications", response_model=list[ApplicationResponse])
async def list_developer_applications(
    dev_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """List all applications for a specific developer."""
    # Verify developer exists
    dev_result = await db.execute(select(Developer).where(Developer.id == dev_id))
    developer = dev_result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")

    # Get applications
    result = await db.execute(
        select(Application)
        .where(Application.developer_id == dev_id)
        .order_by(Application.created_at.desc())
    )
    applications = result.scalars().all()
    return applications


@router.patch("/applications/{id}", response_model=ApplicationResponse)
async def update_application_status(
    id: uuid.UUID,
    update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update application status (pending→reviewed→shortlisted→rejected→hired)."""
    result = await db.execute(select(Application).where(Application.id == id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application.status = update.status
    await db.commit()
    await db.refresh(application)
    return application
