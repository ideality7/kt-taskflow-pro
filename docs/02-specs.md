# 02 — Specs

> 이 문서는 **무엇으로, 어떤 규격으로 만드는가**를 정의한다.
> 선택 이유·아키텍처 결정은 `03-design.md`에서 다룬다.

---

## Task 모델

### 필드 정의

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| `id` | `INTEGER` | PK, AUTO_INCREMENT | 태스크 고유 식별자 |
| `title` | `VARCHAR(200)` | NOT NULL | 태스크 제목 (필수) |
| `description` | `TEXT` | NULL 허용 | 상세 설명 (선택) |
| `status` | `ENUM` | NOT NULL, DEFAULT `'todo'` | `todo` \| `in_progress` \| `done` |
| `due_at` | `DATETIME` | NULL 허용, UTC 저장 | 마감시각 (선택) |
| `created_at` | `DATETIME` | NOT NULL, DEFAULT NOW() | 생성 시각 (UTC) |
| `updated_at` | `DATETIME` | NOT NULL, AUTO UPDATE | 수정 시각 (UTC) |

### status 값 정의

```
todo  →  in_progress  →  done
```

| 값 | 의미 |
|----|------|
| `todo` | 시작 전 (기본값) |
| `in_progress` | 진행 중 |
| `done` | 완료 |

### due_at 규칙

- 클라이언트는 ISO 8601 형식으로 전송한다: `2026-05-12T18:00:00.000Z`
- DB에는 UTC로 저장한다.
- UI 표시는 로컬 타임존 기준 `YYYY-MM-DD HH:mm` 형식을 사용한다: `2026-05-12 18:00`
- 생략 가능(nullable). 생략 시 마감시각 없음으로 처리한다.

---

## 유효성 검증

### 400 Bad Request 조건

| 필드 | 위반 조건 |
|------|-----------|
| `title` | 누락, 빈 문자열, 200자 초과 |
| `status` | `todo` \| `in_progress` \| `done` 외 값 |
| `due_at` | ISO 8601 형식 위반, 파싱 불가 문자열 |

### 404 Not Found 조건

- `id`에 해당하는 태스크가 DB에 존재하지 않을 때

### 에러 응답 형식

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "title은 200자 이하여야 합니다.",
    "field": "title"
  }
}
```

| `code` 값 | HTTP | 설명 |
|-----------|------|------|
| `VALIDATION_ERROR` | 400 | 필드 형식·필수값 위반 |
| `NOT_FOUND` | 404 | 존재하지 않는 id |
| `INTERNAL_ERROR` | 500 | 서버 내부 오류 |

---

## REST API 명세

### 공통 규칙

| 항목 | 규칙 |
|------|------|
| Base URL | `/api/tasks` |
| Content-Type | `application/json` |
| 날짜 형식 | ISO 8601 UTC (`2026-05-12T09:00:00.000Z`) |
| 인증 | MVP 단계 없음 (확장 단계에서 JWT 추가) |

---

### 1. 태스크 생성

```
POST /api/tasks
```

**Request Body**

```json
{
  "title": "디자인 시안 검토",
  "description": "메인 페이지 디자인 시안 피드백 정리",
  "status": "todo",
  "due_at": "2026-05-12T09:00:00.000Z"
}
```

| 필드 | 필수 | 설명 |
|------|------|------|
| `title` | ✅ | VARCHAR(200) |
| `description` | ❌ | 생략 시 null |
| `status` | ❌ | 생략 시 `todo` |
| `due_at` | ❌ | 생략 시 null |

**Response `201 Created`**

```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "메인 페이지 디자인 시안 피드백 정리",
  "status": "todo",
  "due_at": "2026-05-12T09:00:00.000Z",
  "created_at": "2026-05-18T01:00:00.000Z",
  "updated_at": "2026-05-18T01:00:00.000Z"
}
```

---

### 2. 태스크 목록 조회

```
GET /api/tasks
```

> `description` 필드를 **제외**한다. 목록 렌더링 성능을 위해 생략.

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `status` | string | 필터 (`todo` \| `in_progress` \| `done`), 생략 시 전체 |

**Response `200 OK`**

```json
[
  {
    "id": 1,
    "title": "디자인 시안 검토",
    "status": "todo",
    "due_at": "2026-05-12T09:00:00.000Z",
    "created_at": "2026-05-18T01:00:00.000Z",
    "updated_at": "2026-05-18T01:00:00.000Z"
  },
  {
    "id": 2,
    "title": "API 문서 작성",
    "status": "in_progress",
    "due_at": null,
    "created_at": "2026-05-18T02:00:00.000Z",
    "updated_at": "2026-05-18T03:00:00.000Z"
  }
]
```

---

### 3. 태스크 단건 조회

```
GET /api/tasks/:id
```

> `description` 필드를 **포함**한다.

**Response `200 OK`**

```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "메인 페이지 디자인 시안 피드백 정리",
  "status": "todo",
  "due_at": "2026-05-12T09:00:00.000Z",
  "created_at": "2026-05-18T01:00:00.000Z",
  "updated_at": "2026-05-18T01:00:00.000Z"
}
```

---

### 4. 태스크 수정

```
PUT /api/tasks/:id
```

> **부분 수정 허용** — 전송한 필드만 업데이트한다. 생략한 필드는 기존 값을 유지한다.

**Request Body** (예시: status만 변경)

```json
{
  "status": "in_progress"
}
```

**Response `200 OK`** — 수정 후 전체 태스크 반환 (`description` 포함)

```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "메인 페이지 디자인 시안 피드백 정리",
  "status": "in_progress",
  "due_at": "2026-05-12T09:00:00.000Z",
  "created_at": "2026-05-18T01:00:00.000Z",
  "updated_at": "2026-05-18T04:30:00.000Z"
}
```

---

### 5. 태스크 삭제

```
DELETE /api/tasks/:id
```

**Response `204 No Content`** — 응답 바디 없음

---

## 화면 명세 (CRUD 4종 UI)

### 1. 추가 — 태스크 생성 폼

- 화면 상단 또는 우측에 항상 노출된 인라인 폼
- 폼 필드:

| 필드 | 입력 타입 | 필수 |
|------|-----------|------|
| `title` | `<input type="text" maxlength="200">` | ✅ |
| `due_at` | `<input type="datetime-local">` | ❌ |
| `status` | `<select>` (todo / in_progress / done) | ✅ (기본 todo) |

- 제출 버튼 클릭 → `POST /api/tasks` → 성공 시 목록에 즉시 추가 (낙관적 업데이트)
- title 비어있으면 제출 버튼 비활성화

---

### 2. 목록 — 태스크 카드 리스트

- 태스크 1개 = 카드 1장
- 카드에 표시할 정보:

| 요소 | 내용 |
|------|------|
| 제목 | `title` |
| 상태 배지 | `status` 값에 따른 색상 배지 |
| 마감시각 | `due_at` → 로컬 타임존 `D-N HH:MM` 형식 |
| 수정 트리거 | 카드 클릭 |
| 삭제 트리거 | 카드 우측 상단 휴지통 아이콘 |

**status 배지 색상**

| status | 배지 색상 |
|--------|-----------|
| `todo` | 회색 |
| `in_progress` | 파란색 |
| `done` | 초록색 |

**D-N 표시 규칙**

| 조건 | 표시 | 색상 |
|------|------|------|
| 마감 24시간 이상 남음 | `D-3 18:00` | 기본 |
| 마감 1시간 이상~24시간 미만 | `D-0 18:00` | 주황색 |
| 마감 1시간 미만 | `D-0 18:00` | 빨간색 |
| 마감 초과 | `D+2 18:00` | 빨간색 + 취소선 |
| due_at 없음 | 표시 안 함 | — |

---

### 3. 수정 — 카드 클릭 → 모달

- 카드(휴지통 아이콘 제외 영역) 클릭 시 수정 모달 열림
- 모달 내 필드: `title`, `description`, `status`, `due_at`
- 변경 후 저장 버튼 → `PUT /api/tasks/:id` → 성공 시 모달 닫힘 + 카드 즉시 갱신
- 저장 중 버튼 로딩 스피너 표시
- ESC 키 또는 모달 외부 클릭 → 변경 취소 후 닫힘
- macOS 스타일: 둥근 모서리, 반투명 backdrop, 부드러운 등장 애니메이션 (`200ms ease-out`)

---

### 4. 삭제 — 휴지통 → 확인 → DELETE

```
카드 휴지통 아이콘 클릭
  → 확인 다이얼로그 ("이 태스크를 삭제할까요?")
    → [취소] 닫힘
    → [삭제] DELETE /api/tasks/:id
               → 성공(204) → 목록에서 카드 제거
```

- 확인 다이얼로그는 `window.confirm` 대신 커스텀 다이얼로그 컴포넌트 사용
- 삭제 버튼 클릭 중 로딩 스피너, 완료 후 자동 닫힘

---

## 기술 스택 요약

> 상세 버전·설치 명령은 `03-design.md`의 셋업 가이드에서 다룬다.

| 레이어 | 기술 |
|--------|------|
| **Frontend** | Next.js 15 (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| **Backend** | Express.js 5 + TypeScript |
| **DB** | SQLite (MVP) → PostgreSQL (확장) |
| **ORM** | Prisma |
| **상태 관리** | TanStack Query (서버 상태) + Zustand (테마 등 클라이언트 상태) |
| **폼** | React Hook Form + Zod |
| **테스트** | Vitest + Playwright |
| **실시간** | 폴링 (`setInterval`, 30초) — WebSocket은 MVP 범위 외 |
