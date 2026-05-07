from fastapi import APIRouter

from app.api.v1 import developers, jobs, companies, applications, search, uploads, stats

router = APIRouter(prefix="/v1")
router.include_router(developers.router)
router.include_router(jobs.router)
router.include_router(companies.router)
router.include_router(applications.router)
router.include_router(search.router)
router.include_router(uploads.router)
router.include_router(stats.router)
