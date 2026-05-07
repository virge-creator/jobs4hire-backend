import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    # Listing
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[str | None] = mapped_column(String(500))

    # Type
    job_type: Mapped[str] = mapped_column(String(32), nullable=False)  # contract, permanent, both
    remote_policy: Mapped[str] = mapped_column(String(32), default="remote")  # remote, onsite, hybrid
    location: Mapped[str | None] = mapped_column(String(255))

    # Compensation — always public
    salary_min: Mapped[int | None] = mapped_column(Integer)
    salary_max: Mapped[int | None] = mapped_column(Integer)
    hourly_rate_min: Mapped[int | None] = mapped_column(Integer)
    hourly_rate_max: Mapped[int | None] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="EUR")

    # Skills
    required_skills: Mapped[list | None] = mapped_column(ARRAY(String(64)))
    nice_to_have_skills: Mapped[list | None] = mapped_column(ARRAY(String(64)))
    seniority: Mapped[str | None] = mapped_column(String(32))
    experience_years_min: Mapped[int | None] = mapped_column(Integer)

    # Status
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # draft, active, closed, expired
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    external: Mapped[bool] = mapped_column(Boolean, default=False)  # curated external listing
    external_url: Mapped[str | None] = mapped_column(String(512))

    # Metadata
    views: Mapped[int] = mapped_column(Integer, default=0)
    application_count: Mapped[int] = mapped_column(Integer, default=0)
    tags: Mapped[list | None] = mapped_column(ARRAY(String(64)))

    # Search
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
