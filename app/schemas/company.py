import uuid
from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    website_url: str | None = None
    description: str | None = None
    location: str | None = None
    industry: str | None = None
    size: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    website_url: str | None = None
    description: str | None = None
    location: str | None = None
    industry: str | None = None
    size: str | None = None


class CompanyRead(CompanyBase):
    id: uuid.UUID
    slug: str
    logo_url: str | None = None
    verified: bool
    response_rate: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
