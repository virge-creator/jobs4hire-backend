import uuid
from datetime import datetime

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str
    short_description: str | None = None
    job_type: str  # contract, permanent, both
    remote_policy: str = "remote"
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    hourly_rate_min: int | None = None
    hourly_rate_max: int | None = None
    currency: str = "EUR"
    required_skills: list[str] | None = None
    nice_to_have_skills: list[str] | None = None
    seniority: str | None = None
    experience_years_min: int | None = None
    tags: list[str] | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    short_description: str | None = None
    job_type: str | None = None
    remote_policy: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    hourly_rate_min: int | None = None
    hourly_rate_max: int | None = None
    currency: str | None = None
    required_skills: list[str] | None = None
    nice_to_have_skills: list[str] | None = None
    seniority: str | None = None
    experience_years_min: int | None = None
    status: str | None = None
    tags: list[str] | None = None


class JobRead(JobBase):
    id: uuid.UUID
    slug: str
    company_id: uuid.UUID
    status: str
    featured: bool
    external: bool
    external_url: str | None = None
    views: int
    application_count: int
    created_at: datetime
    expires_at: datetime | None = None

    model_config = {"from_attributes": True}


class JobList(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    company_id: uuid.UUID
    job_type: str
    remote_policy: str
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    hourly_rate_min: int | None = None
    hourly_rate_max: int | None = None
    currency: str
    required_skills: list[str] | None = None
    seniority: str | None = None
    featured: bool
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
