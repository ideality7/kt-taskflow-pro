from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers.tasks import router as tasks_router

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow Pro API",
    description="팀 업무관리 풀스택 웹앱 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP 단계 — 확장 시 도메인 제한
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)


@app.get("/health")
def health():
    return {"status": "ok"}
