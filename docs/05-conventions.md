# 05 — Conventions

> 이 문서는 **어떻게 작성하고 협업하는가**를 정의한다.
> 설계 결정은 `03-design.md`, 작업 계획은 `04-tasks.md`에서 다룬다.

---

## 명명 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| 백엔드 변수·함수·파일 | `snake_case` | `task_id`, `get_task_by_id`, `task_router.py` |
| 프론트엔드 변수·함수 | `camelCase` | `taskId`, `getTaskById`, `renderTaskList` |
| 프론트엔드 컴포넌트 함수 | `PascalCase` | `TaskCard`, `ConfirmDialog` |
| 상수 | `UPPER_SNAKE_CASE` | `MAX_TITLE_LENGTH`, `POLL_INTERVAL_MS` |
| DB 컬럼 (SQLAlchemy) | `snake_case` | `due_at`, `created_at` |
| API 응답 키 | `snake_case` | `{ "due_at": "...", "created_at": "..." }` |

### 언어 규칙

| 대상 | 언어 |
|------|------|
| 코드 식별자 (변수·함수·클래스·파일명) | **영어** |
| 주석 | **한국어** |
| 커밋 메시지 요약 | **한국어** |
| 문서 (docs/) | **한국어** |

```python
# 좋음
# 마감일이 지난 태스크는 빨간색으로 강조한다
def is_overdue(due_at: datetime) -> bool:
    return due_at < datetime.utcnow()

# 나쁨 — 주석을 영어로 작성
# Check if task is overdue
def is_overdue(due_at: datetime) -> bool:
    return due_at < datetime.utcnow()
```

---

## 금지 항목

| # | 금지 | 이유 | 대안 |
|---|------|------|------|
| 1 | `print()` 디버깅 | 프로덕션 로그에 노이즈 유입, 민감 정보 노출 위험 | `logging` 모듈 사용 (`logger.debug()`, `logger.info()`) |
| 2 | `bare except` (`except:`) | 모든 예외를 삼켜 오류 원인 추적 불가 | `except SpecificError as e:` 로 예외 타입 명시 |
| 3 | 비밀번호·시크릿 하드코딩 | 코드 노출 시 즉시 보안 사고, git 히스토리에 영구 기록 | `.env` 파일에 저장, `os.getenv('KEY')` 로 참조 |
| 4 | TypeScript `any` 타입 | 타입 안전성 상실, 런타임 오류를 컴파일 타임에 잡지 못함 | 명시적 타입 또는 `unknown` + 타입 가드 사용 |
| 5 | CSS `!important` | 우선순위 체계 붕괴, 이후 스타일 재정의 불가 | 셀렉터 구체성 개선 또는 Tailwind 유틸리티 클래스 조정 |

### 금지 예시

```python
# 금지 1 — print 디버깅
print(f"태스크 조회: {task_id}")  # ❌

# 대안
import logging
logger = logging.getLogger(__name__)
logger.debug("태스크 조회: %s", task_id)  # ✅

# 금지 2 — bare except
try:
    task = get_task(task_id)
except:          # ❌ 모든 예외 삼킴
    pass

# 대안
try:
    task = get_task(task_id)
except TaskNotFoundError as e:   # ✅
    raise HTTPException(status_code=404, detail=str(e))

# 금지 3 — 하드코딩
SECRET_KEY = "my-secret-key-1234"  # ❌

# 대안
import os
SECRET_KEY = os.getenv("SECRET_KEY")  # ✅
```

---

## 테스트 규칙

### 도구

| 용도 | 도구 |
|------|------|
| 백엔드 단위·통합 테스트 | `pytest` + `httpx` (FastAPI `TestClient`) |
| 프론트엔드 | (MVP 단계: 수동 확인, 확장 단계에서 Playwright 도입 검토) |

### 필수 테스트 케이스

모든 API 엔드포인트는 아래 3종 케이스를 반드시 작성한다.

| 케이스 | 설명 | 예상 응답 |
|--------|------|-----------|
| **정상** | 유효한 요청 | 2xx + 올바른 응답 바디 |
| **404** | 존재하지 않는 `id` | `404 Not Found` |
| **400 / 422** | 필수 필드 누락 또는 형식 위반 | `400` 또는 `422 Unprocessable Entity` |

```python
# 예시 — POST /api/tasks 테스트
def test_create_task_success(client):
    # 정상 케이스
    response = client.post("/api/tasks", json={"title": "테스트 태스크"})
    assert response.status_code == 201
    assert response.json()["title"] == "테스트 태스크"

def test_create_task_missing_title(client):
    # 400 / 422 케이스 — title 누락
    response = client.post("/api/tasks", json={})
    assert response.status_code in (400, 422)

def test_get_task_not_found(client):
    # 404 케이스
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404
```

### 테스트 파일 위치

```
backend/
└── tests/
    ├── conftest.py        # fixture (TestClient, 테스트 DB)
    ├── test_create.py     # POST /api/tasks
    ├── test_list.py       # GET /api/tasks
    ├── test_get.py        # GET /api/tasks/{id}
    ├── test_update.py     # PUT /api/tasks/{id}
    └── test_delete.py     # DELETE /api/tasks/{id}
```

### 테스트 완료 기준

- `pytest` 실행 시 전체 PASS
- 테스트 없이 Phase 완료로 간주하지 않는다 (`04-tasks.md` 절대 규칙 3번)

---

## Git 커밋 규칙

### 형식

```
<type>: <한국어 요약>
```

- type은 영어, 요약은 **한국어**
- 요약은 50자 이하, 명령형으로 작성 ("추가", "수정", "제거")
- 본문이 필요한 경우 빈 줄 하나 후 작성

### type 목록

| type | 사용 시점 | 예시 |
|------|-----------|------|
| `feat` | 새 기능 추가 | `feat: 태스크 생성 API 추가` |
| `fix` | 버그 수정 | `fix: due_at 없을 때 500 오류 수정` |
| `docs` | 문서 변경 | `docs: 02-specs API 명세 보완` |
| `refactor` | 동작 변화 없는 코드 개선 | `refactor: task 서비스 함수 분리` |
| `test` | 테스트 추가·수정 | `test: PUT /api/tasks 404 케이스 추가` |
| `chore` | 빌드·설정·의존성 변경 | `chore: requirements.txt 업데이트` |

### 커밋 금지 사항

| 금지 | 이유 |
|------|------|
| `fix: fix bug` | 무의미한 요약 |
| 하나의 커밋에 feat + fix 혼재 | type 의미 훼손 |
| `.env` 파일 커밋 | 시크릿 노출 |
| 테스트 실패 상태로 커밋 | CI 기준 위반 |

### 브랜치 전략 (MVP 단계)

MVP 단계에서는 단일 `main` 브랜치에서 작업한다.
확장 단계 진입 시 `feat/*` 브랜치 전략을 도입한다.

---

## .gitignore 필수 항목

```
# 시크릿
.env
.env.local

# Python
__pycache__/
*.pyc
venv/
.venv/
*.egg-info/

# SQLite
*.db
*.sqlite3

# 에디터
.vscode/
.idea/
*.swp
```
