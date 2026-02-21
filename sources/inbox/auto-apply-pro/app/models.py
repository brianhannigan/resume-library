from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    datetime_utc: datetime
    company: str
    title: str
    source: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    status: str = "parsed"  # parsed|generated|submitted|error|skipped
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    profile_used: Optional[str] = None
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    notes: Optional[str] = None
    error: Optional[str] = None

class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int
    ts: datetime
    event_type: str
    message: str
    json_blob: Optional[str] = None
