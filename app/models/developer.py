import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Developer(Base):
    __tablename__ = "developers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identity
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512))
    location: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str | None] = mapped_column(String(64))
    bio: Mapped[str | None] = mapped_column(Text)

    # Availability
    availability: Mapped[str] = mapped_column(String(32), default="open")  # open_contract, open_fulltime, both, not_looking
    hourly_rate_min: Mapped[int | None] = mapped_column(Integer)
    hourly_rate_max: Mapped[int | None] = mapped_column(Integer)
    daily_rate_min: Mapped[int | None] = mapped_column(Integer)
    daily_rate_max: Mapped[int | None] = mapped_column(Integer)
    salary_min: Mapped[int | None] = mapped_column(Integer)
    salary_max: Mapped[int | None] = mapped_column(Integer)
    remote_preference: Mapped[str] = mapped_column(String(32), default="remote")  # remote, onsite, hybrid
    languages_spoken: Mapped[list | None] = mapped_column(ARRAY(String(32)))

    # Skills & experience
    skills: Mapped[dict | None] = mapped_column(JSONB, default=dict)  # {"python": 5, "react": 3}
    total_years_experience: Mapped[int | None] = mapped_column(Integer)
    seniority: Mapped[str | None] = mapped_column(String(32))  # junior, mid, senior, staff, principal
    domains: Mapped[list | None] = mapped_column(ARRAY(String(64)))  # fintech, healthtech, etc.

    # Social / portfolio
    github_username: Mapped[str | None] = mapped_column(String(255))
    github_data: Mapped[dict | None] = mapped_column(JSONB)  # auto-imported repos, languages, activity
    linkedin_url: Mapped[str | None] = mapped_column(String(512))
    website_url: Mapped[str | None] = mapped_column(String(512))
    resume_url: Mapped[str | None] = mapped_column(String(512))

    # Work history & endorsements
    work_history: Mapped[list | None] = mapped_column(JSONB, default=list)
    endorsements: Mapped[list | None] = mapped_column(JSONB, default=list)

    # Verification
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    github_linked: Mapped[bool] = mapped_column(Boolean, default=False)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Auth
    workos_user_id: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)

    # Search
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    applications = relationship("Application", back_populates="developer")
