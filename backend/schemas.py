from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from models import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    due_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title은 공백만으로 이루어질 수 없습니다")
        return v


class TaskUpdate(BaseModel):
    # 부분 수정 허용 — 모든 필드 선택
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("title은 공백만으로 이루어질 수 없습니다")
        return v


class TaskListItem(BaseModel):
    # 목록 응답 — description 제외
    id: int
    title: str
    status: TaskStatus
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    # 단건·수정 응답 — description 포함
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
