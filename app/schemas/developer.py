import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class DeveloperBase(BaseModel):
    full_name: str
    location: str | None = None
    timezone: str | None = None
    bio: str | None = None
    availability: str = "open"
    hourly_rate_min: int | None = None
    hourly_rate_max: int | None = None
    daily_rate_min: int | None = None
    daily_rate_max: int | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    remote_preference: str = "remote"
    languages_spoken: list[str] | None = None
    skills: dict[str, int] | None = None
    total_years_experience: int | None = None
    seniority: str | None = None
    domains: list[str] | None = None
    github_username: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None


class DeveloperCreate(DeveloperBase):
    email: EmailStr


class DeveloperUpdate(DeveloperBase):
    full_name: str | None = None  # type: ignore[assignment]


class DeveloperRead(DeveloperBase):
    id: uuid.UUID
    email: str
    avatar_url: str | None = None
    github_linked: bool = False
    email_verified: bool = False
    created_at: datetime
    last_active_at: datetime | None = None

    model_config = {"from_attributes": True}


class DeveloperList(BaseModel):
    id: uuid.UUID
    full_name: str
    avatar_url: str | None = None
    location: str | None = None
    availability: str
    seniority: str | None = None
    skills: dict[str, int] | None = None
    hourly_rate_min: int | None = None
    hourly_rate_max: int | None = None
    remote_preference: str

    model_config = {"from_attributes": True}
