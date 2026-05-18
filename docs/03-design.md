# 03 — Design

> 이 문서는 **왜 이렇게 설계했는가**를 정의한다.
> 기술 스택 명세는 `02-specs.md`, 작업 계획은 `04-tasks.md`에서 다룬다.

---

## 의존성 추가 정책

> **이 문서에 선택 사유를 먼저 기록하기 전까지 새 의존성 도입은 금지한다.**

새 라이브러리·패키지를 추가해야 할 경우:

1. 아래 결정 기록 표 형식으로 항목을 추가한다.
2. 선택·대안·근거·트레이드오프를 작성한다.
3. 사용자 승인 후 설치한다.

승인 없는 `pip install` / `npm install` 금지.

---

## 아키텍처 결정 기록 (ADR)

### ADR-001. 백엔드 프레임워크

| 항목 | 내용 |
|------|------|
| **선택** | FastAPI |
| **대안** | Django, Express.js |
| **근거** | Python 타입 힌트 기반 자동 유효성 검증(Pydantic), `/docs` OpenAPI UI 즉시 제공, 비동기 I/O 내장. Django는 ORM·admin 등 MVP에 불필요한 기능이 과다. Express는 Python DB 생태계(SQLAlchemy)와 조합이 어색함. |
| **트레이드오프** | Node.js 생태계(npm 패키지)와 단절. ASGI 서버(uvicorn) 별도 관리 필요. |

---

### ADR-002. 프론트엔드

| 항목 | 내용 |
|------|------|
| **선택** | Vanilla JS + Tailwind CDN |
| **대안** | React, Vue |
| **근거** | MVP 화면 4종(추가·목록·수정·삭제)은 컴포넌트 트리 없이 DOM 조작만으로 충분. 빌드 도구·번들러 없이 HTML 파일 하나로 실행 가능해 배포·디버깅 마찰이 없음. Tailwind CDN은 프로토타입 단계에서 별도 빌드 불필요. |
| **트레이드오프** | 화면이 복잡해질수록 상태-DOM 동기화 코드가 늘어남. 컴포넌트 재사용 어려움. 확장 단계(Kanban, 채팅)에서 React 전환 검토 필요. |

---

### ADR-003. 데이터베이스

| 항목 | 내용 |
|------|------|
| **선택** | SQLite (MVP) → PostgreSQL (확장), ORM: SQLAlchemy |
| **대안** | 처음부터 PostgreSQL, Prisma(Node) |
| **근거** | SQLite는 파일 하나로 로컬 실행 가능 — Docker 없이 개발 시작. SQLAlchemy는 SQLite·PostgreSQL 모두 지원하므로 DB 교체 시 연결 문자열 변경만으로 충분. 스키마는 Alembic 마이그레이션으로 관리. |
| **트레이드오프** | SQLite는 동시 쓰기 처리량이 낮음(WAL 모드로 완화). 확장 시 PostgreSQL 전환 마이그레이션 1회 필수. |

---

### ADR-004. CSS 방식

| 항목 | 내용 |
|------|------|
| **선택** | Tailwind CSS 유틸리티 클래스 단독 사용 |
| **대안** | styled-components, CSS Modules, 일반 CSS |
| **근거** | 유틸리티 클래스는 HTML에서 스타일을 바로 읽을 수 있어 맥락 전환 없음. 다크모드는 `dark:` 변형만으로 처리 가능. Vanilla JS 환경에서 styled-components는 JS 런타임 의존성으로 오버헤드 발생. |
| **트레이드오프** | 클래스 문자열이 길어져 HTML 가독성 저하 가능. 커스텀 디자인 토큰은 `tailwind.config`에 집중 관리해야 함. |
| **금지** | `styled-components` 도입 금지 — Vanilla JS 환경에서 불필요한 런타임 CSS-in-JS |

---

### ADR-005. 실시간 업데이트

| 항목 | 내용 |
|------|------|
| **선택** | 폴링 (`setInterval`, 3초 간격) |
| **대안** | WebSocket, SSE(Server-Sent Events) |
| **근거** | MVP 규모(10인 팀)에서 3초 폴링은 서버 부하가 수용 가능한 수준. 구현이 단순하고 디버깅이 쉬움. WebSocket은 연결 관리·재연결 로직이 추가되어 MVP 복잡도를 높임. |
| **트레이드오프** | 데이터 변경 없어도 3초마다 요청 발생. 서버 부하 누적. 확장 단계에서 SSE 또는 WebSocket으로 교체 예정. |
| **보류** | WebSocket — 확장 4단계(채팅) 구현 시 재검토 |

---

### ADR-006. 상태 관리

| 항목 | 내용 |
|------|------|
| **선택** | 모듈 변수 + DOM 직접 갱신 |
| **대안** | Redux, Zustand, Jotai, MobX |
| **근거** | Vanilla JS 환경에서 상태 관리 라이브러리는 번들러 없이 사용하기 어려움. `tasks` 배열을 모듈 스코프 변수로 보관하고 변경 시 `renderTaskList()` 함수를 직접 호출하면 충분. 단방향 흐름(상태 변경 → 전체 재렌더)을 함수 호출 규칙으로 강제함. |
| **트레이드오프** | 상태 변경 추적이 어렵고 버그 발생 시 디버깅 난이도 높음. 화면이 늘어날수록 재렌더 범위 관리가 복잡해짐. React 전환 시 상태 로직 재작성 필요. |

---

### ADR-007. 디자인 시스템

| 항목 | 내용 |
|------|------|
| **선택** | macOS UI 톤 자체 구현 |
| **대안** | Material UI, Ant Design |
| **근거** | Material·Ant Design은 자체 디자인 언어가 강해 macOS 톤 구현 시 토큰 오버라이드 비용이 큼. Tailwind 유틸리티만으로 macOS 스타일을 직접 구현하면 불필요한 컴포넌트 라이브러리 의존성이 없음. |
| **트레이드오프** | 공통 컴포넌트(모달, 드롭다운 등)를 직접 구현해야 함. 접근성(ARIA) 처리를 수동으로 해야 함. |

**디자인 토큰 (Tailwind 클래스 매핑)**

| 토큰 | Tailwind 클래스 | 설명 |
|------|-----------------|------|
| 모서리 | `rounded-xl` (`border-radius: 12px`) | 카드·모달 기본 |
| 모서리 소형 | `rounded-lg` (`border-radius: 8px`) | 버튼·배지 |
| 그림자 | `shadow-lg` | 카드 기본 그림자 |
| 그림자 강조 | `shadow-xl` | 모달·드롭다운 |
| 반투명 배경 | `bg-white/70 backdrop-blur-md` | 카드 배경 (라이트) |
| 반투명 배경 다크 | `dark:bg-zinc-800/70 backdrop-blur-md` | 카드 배경 (다크) |
| 폰트 | `font-sans` | 시스템 폰트 (`-apple-system, BlinkMacSystemFont, 'Segoe UI'`) |
| 터치 타겟 | `min-h-[44px] min-w-[44px]` | 모든 인터랙티브 요소 최소 크기 |
| 애니메이션 | `transition-all duration-150 ease-out` | 기본 전환 |
| 모달 등장 | `duration-200 ease-out` | 모달 진입 애니메이션 |

---

### ADR-008. 라이트 / 다크 테마

| 항목 | 내용 |
|------|------|
| **선택** | Tailwind `dark:` 변형 + `localStorage('theme')` |
| **대안** | CSS 변수 단독, 별도 CSS 파일 분기 |
| **근거** | Tailwind `dark:` 변형은 `<html class="dark">` 하나만 토글하면 전체 다크 스타일이 적용됨. 구현이 단순하고 클래스 파악이 즉시 가능. CSS 변수 방식 대비 학습 비용 낮음. |
| **트레이드오프** | `dark:` 클래스가 모든 요소에 추가돼 HTML이 길어짐. Tailwind JIT 빌드 없이 CDN 사용 시 사용되지 않는 클래스도 모두 포함됨. |

**구현 규칙**

```js
// 1. 초기값: localStorage 우선, 없으면 시스템 설정
const saved = localStorage.getItem('theme')
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
const theme = saved ?? (prefersDark ? 'dark' : 'light')
document.documentElement.classList.toggle('dark', theme === 'dark')

// 2. 토글
function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark')
  localStorage.setItem('theme', isDark ? 'dark' : 'light')
}
```

**SSR 깜빡임 방지 (향후 Next.js 전환 시 적용)**

```html
<!-- <head> 최상단 인라인 스크립트로 HTML 클래스 선적용 -->
<script>
  const t = localStorage.getItem('theme')
  if (t === 'dark' || (!t && matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
  }
</script>
```

---

## 결정 요약표

| # | 결정 영역 | 선택 | 핵심 근거 |
|---|-----------|------|-----------|
| 001 | 백엔드 | FastAPI | 타입 기반 자동 검증, OpenAPI 자동 생성 |
| 002 | 프론트엔드 | Vanilla JS + Tailwind CDN | 빌드 없이 실행, MVP 복잡도 최소화 |
| 003 | DB | SQLite → PostgreSQL + SQLAlchemy | 파일 DB로 시작, 연결 문자열만 바꿔 전환 |
| 004 | CSS | Tailwind 단독 | styled-components 런타임 불필요 |
| 005 | 실시간 | 폴링 3초 | WebSocket 대비 구현 단순, MVP 규모 충분 |
| 006 | 상태 | 모듈 변수 + DOM 갱신 | 라이브러리 없이 단방향 흐름 유지 |
| 007 | 디자인 | macOS 톤 자체 구현 | Material·Ant 오버라이드 비용 제거 |
| 008 | 테마 | dark: 변형 + localStorage | 토글 하나로 전체 적용, 새로고침 유지 |
