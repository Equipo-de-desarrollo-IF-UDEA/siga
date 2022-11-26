from typing import Any
from datetime import datetime

from pydantic import BaseModel, validator, Field

from app.domain.schemas.application import ApplicationResponse


class PermissionBase(BaseModel):
    start_date: datetime
    end_date: datetime
    justification: str = Field(max_length=300, min_length=30)
    documents: list[Any] | None


class PermissionCreate(PermissionBase):
    application_sub_type_id: int


class PermissionUpdate(PermissionBase):
    application_sub_type_id: int


class PermissionResponse(ApplicationResponse):
    permission: PermissionBase