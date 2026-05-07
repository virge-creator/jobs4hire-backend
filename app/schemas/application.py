import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationBase(BaseModel):
    cover_letter: str | None = None


class ApplicationCreate(ApplicationBase):
    developer_id: uuid.UUID


class ApplicationUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|reviewed|shortlisted|rejected|hired)$")


class ApplicationResponse(ApplicationBase):
    id: uuid.UUID
    job_id: uuid.UUID
    developer_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
