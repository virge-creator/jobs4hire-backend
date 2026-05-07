from fastapi import APIRouter

from app.api.v1 import developers, jobs, companies

router = APIRouter(prefix="/v1")
router.include_router(developers.router)
router.include_router(jobs.router)
router.include_router(companies.router)
