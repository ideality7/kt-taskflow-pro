from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Task, TaskStatus
from schemas import TaskCreate, TaskUpdate, TaskListItem, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(body: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=body.title,
        description=body.description,
        status=body.status,
        due_at=body.due_at,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskListItem])
def list_tasks(
    status: Optional[TaskStatus] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.order_by(Task.created_at.desc()).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="태스크를 찾을 수 없습니다")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="태스크를 찾을 수 없습니다")

    # 전송된 필드만 업데이트 (부분 수정)
    data = body.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="태스크를 찾을 수 없습니다")
    db.delete(task)
    db.commit()
