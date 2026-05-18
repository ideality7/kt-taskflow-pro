# 04 — Tasks

> MVP를 3개 Phase로 진행한다. 확장 단계는 이 문서에 포함하지 않는다.
> 진행 규칙: **순서대로만 진행. 병렬 금지. 단계별 검증 필수.**

---

## 진행 규칙

| 규칙 | 내용 |
|------|------|
| 순서 | 위에서 아래로, 이전 단계 검증 통과 후 다음 단계 진행 |
| 병렬 금지 | 두 단계를 동시에 진행하지 않는다 |
| 검증 필수 | 각 단계의 검증 방법을 실제로 확인한 후 ✅ 표시 |
| 수정 발생 시 | 현재 단계 재검증 통과 후 다음 단계로 |
| 완료 기준 | Phase 3 마지막 단계(git push) 완료 |

---

## 상태 범례

| 아이콘 | 상태 |
|--------|------|
| `✅` | 완료 (검증 통과) |
| `🔵` | 진행 중 |
| `⬜` | 미시작 |

---

## Phase 1 — 설계 (완료)

> 목표: Claude가 작업 전 읽을 수 있는 문서 기반 완성

| # | 단계 | 작업 내용 | 검증 방법 | 상태 |
|---|------|-----------|-----------|------|
| 1-1 | CLAUDE.md 작성 | 역할·절대규칙·모호한 요청 처리 방식 정의 | `CLAUDE.md` 파일 존재, 5개 절대 규칙 항목 확인 | ✅ |
| 1-2 | docs/ 폴더 생성 | `docs/` 디렉토리 생성 | `ls docs/` 로 폴더 존재 확인 | ✅ |
| 1-3 | 00-overview.md 작성 | 6개 문서 매핑표, 읽는 순서, 관심사 분리 설명 | 파일 내 매핑표·읽는 순서·분리 사유 3항목 모두 존재 | ✅ |
| 1-4 | 01-product.md 작성 | 목표·페르소나·MVP 범위·UI 톤·성공 기준 정의 | 성공 기준 6개 항목 모두 존재 | ✅ |
| 1-5 | 02-specs.md 작성 | Task 모델 필드·API 5개·화면 명세 정의 | 필드 7개, API 5개, 화면 명세 4종 항목 존재 | ✅ |
| 1-6 | 03-design.md 작성 | ADR 8개 결정표 (선택/대안/근거/트레이드오프) | ADR 001~008 전항목, 의존성 추가 정책 존재 | ✅ |
| 1-7 | 04-tasks.md 작성 | Phase 1~3 체크리스트, 단계별 검증 방법 | Phase별 단계 수 (10·10·8), 검증 방법 열 존재 | ✅ |
| 1-8 | 05-conventions.md 작성 | 코딩 컨벤션·네이밍·Git 커밋·PR 기준 | 커밋 type 목록, 브랜치 전략, PR 머지 조건 존재 | ✅ |
| 1-9 | 문서 교차 검증 | 6개 문서 간 용어·필드명 일치 확인 | `task` 필드명이 02·03 문서에서 동일하게 사용됨 | ✅ |
| 1-10 | git 초기화 및 첫 push | `git init`, 로컬 설정, remote 등록, `git push` | GitHub 저장소에 파일 존재 확인 | ✅ |

---

## Phase 2 — 백엔드

> 목표: FastAPI CRUD API 5개 구현, Swagger(`/docs`)에서 전 엔드포인트 동작 확인

| # | 단계 | 작업 내용 | 검증 방법 | 상태 |
|---|------|-----------|-----------|------|
| 2-1 | 폴더 생성 | `backend/` 디렉토리 생성, Python 가상환경 구성 | `backend/venv/` 존재, `python --version` 출력 확인 | ⬜ |
| 2-2 | 의존성 설치 | `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `pydantic` 설치, `requirements.txt` 작성 | `pip list`에 5개 패키지 모두 출력 | ⬜ |
| 2-3 | DB 설정 | SQLite 연결, SQLAlchemy `engine`·`SessionLocal`·`Base` 구성 | `backend/database.py` 존재, `tasks.db` 파일 생성 확인 | ⬜ |
| 2-4 | Task 모델 정의 | SQLAlchemy ORM 모델 — 7개 필드 (`id`, `title`, `description`, `status`, `due_at`, `created_at`, `updated_at`) | `alembic upgrade head` 성공, DB에 `tasks` 테이블 생성 확인 | ⬜ |
| 2-5 | Pydantic 스키마 정의 | `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskListItem` 스키마 작성 | `title` 누락 시 422 반환, `status` 이상값 시 422 반환 확인 | ⬜ |
| 2-6 | `POST /api/tasks` 구현 | 태스크 생성, 201 반환 | Swagger에서 요청 후 201 응답, DB에 레코드 존재 확인 | ⬜ |
| 2-7 | `GET /api/tasks` 구현 | 목록 조회 (`description` 제외), 200 반환, `?status=` 필터 | Swagger에서 전체·필터 조회 200 응답, `description` 필드 없음 확인 | ⬜ |
| 2-8 | `GET /api/tasks/{id}` 구현 | 단건 조회 (`description` 포함), 200 / 존재하지 않는 id 404 반환 | 존재 id → 200 + `description` 있음 / 없는 id → 404 확인 | ⬜ |
| 2-9 | `PUT /api/tasks/{id}` 구현 | 부분 수정, 200 반환 / 없는 id 404 반환 | `status`만 전송 시 나머지 필드 유지 확인, `updated_at` 갱신 확인 | ⬜ |
| 2-10 | `DELETE /api/tasks/{id}` 구현 | 삭제, 204 반환 / 없는 id 404 반환 | 204 응답 바디 없음 확인, 이후 GET 시 404 반환 확인 | ⬜ |

**Phase 2 완료 기준**

- `uvicorn backend.main:app --reload` 실행 후 `http://127.0.0.1:8000/docs` 접속
- Swagger UI에서 5개 엔드포인트 전부 수동 실행 → 전부 정상 응답
- 없는 id 요청 → 404, 잘못된 `status` 값 → 422(또는 400) 확인

---

## Phase 3 — 프론트엔드

> 목표: HTML + Vanilla JS + Tailwind CDN으로 메인 화면 구현, API 연결, git push

| # | 단계 | 작업 내용 | 검증 방법 | 상태 |
|---|------|-----------|-----------|------|
| 3-1 | 폴더 및 HTML 기본 구조 | `frontend/index.html` 생성, Tailwind CDN 연결, 시스템 폰트·다크모드 클래스 설정 | 브라우저에서 파일 열기, 콘솔 오류 없음, 빈 화면 정상 렌더 확인 | ⬜ |
| 3-2 | 테마 토글 구현 | 헤더 토글 버튼, `localStorage('theme')` 저장, `prefers-color-scheme` 초기값, `dark:` 변형 적용 | 토글 클릭 후 배경색 전환 확인, 새로고침 후 테마 유지 확인 | ⬜ |
| 3-3 | 태스크 추가 폼 구현 | `title`(필수)·`due_at`·`status` 입력 폼, `title` 비어있으면 버튼 비활성화 | 빈 title로 제출 불가 확인, 360px에서 폼 레이아웃 깨짐 없음 확인 | ⬜ |
| 3-4 | `POST /api/tasks` 연결 | 폼 제출 → API 호출 → 201 응답 시 목록 갱신 | 네트워크 탭에서 201 확인, 제출 직후 목록에 추가 확인 | ⬜ |
| 3-5 | 태스크 목록 렌더링 | `GET /api/tasks` 호출, 카드 렌더, status 배지 색상, D-N HH:MM 마감 표시 | 카드 목록 출력, 배지 3종 색상 확인, due_at 있는 항목 D-N 표시 확인 | ⬜ |
| 3-6 | 폴링 구현 | `setInterval` 3초, 목록 자동 갱신 | 다른 탭에서 태스크 추가 후 3초 내 목록 자동 반영 확인 | ⬜ |
| 3-7 | 수정 모달 구현 | 카드 클릭 → 모달 열림, `title`·`description`·`status`·`due_at` 편집, `PUT /api/tasks/{id}` 연결, ESC·외부 클릭 닫힘 | 수정 저장 후 카드 즉시 갱신 확인, ESC로 닫힘 확인, 360px에서 모달 깨짐 없음 확인 | ⬜ |
| 3-8 | 삭제 구현 및 git push | 휴지통 클릭 → 커스텀 확인 다이얼로그 → `DELETE /api/tasks/{id}` → 204 → 카드 제거, 전체 검증 후 `git push` | 삭제 후 카드 사라짐 확인, 성공 기준 6개 항목 전부 통과 후 push | ⬜ |

**Phase 3 완료 기준 (= MVP DoD)**

| # | 기준 | 검증 방법 |
|---|------|-----------|
| 1 | 새로고침 후 데이터 유지 | 새로고침 후 태스크 목록 동일 |
| 2 | 360px 레이아웃 정상 | Chrome DevTools 360px 뷰포트 수동 확인 |
| 3 | CRUD API 200ms 이내 | 로컬 기준 Network 탭 Timing 확인 |
| 4 | CRUD 4종 화면 동작 | 추가·목록·수정·삭제 시나리오 수동 통과 |
| 5 | 테마 토글 + 새로고침 유지 | 토글 → 새로고침 → 동일 테마 |
| 6 | 마감시각 날짜+시간 표시 | `2026-05-12 18:00` 형식 화면 표시 |
