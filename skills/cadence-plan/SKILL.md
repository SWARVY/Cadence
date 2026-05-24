---
name: cadence-plan
description: 개인 플랜 단계 정확도 부스터. 큰 작업, 신규 spec 작성, 모호 작업 시작, 추상화 결정 시 4단 체크리스트를 적용한다. 컨텍스트 수집 / 옵션 2안 + Contrarian / 위험·폐기·Out of scope / 외부 검증 사다리. 스펙시트 생성 시 brainstorming / writing 계열 helper lens 를 lazy-load 하되, 결정권은 cadence-plan 에 둔다. 프로젝트 무관, cwd 의 docs/retrospectives/ docs/ai-rules/ 메모리를 동적 스캔.
---

# cadence-plan

플랜 단계 결함 패턴 사전 차단용 4단 mandatory 체크리스트. 회고에서 반복적으로 발견된 *플랜 단계 실패 모드* 를 룰화.

## 언제 적용하나

다음 중 1+ 조건 충족 시 mandatory:
- 큰 작업 (≥ 30분 / 여러 파일 / 새 도메인 / 추상화)
- 신규 spec / specsheet draft 작성 (특히 새 도메인·모호 범위)
- 새 도메인 / 새 컴포넌트 / 새 라우트 추가
- 추상화 결정 (재사용 컴포넌트 분리, 헬퍼 추출 등)
- 모호한 요구 (server contract / 디자인 미확정) 진입
- mid-PR 스코프 변경 검토

**압축 대상**: 중간 작업 (10-30분 / 단일 feature) 은 4단 전체를 강제하지 않고 2-3단으로 묶는다.

**제외 대상**: 1줄 fix, 봇 follow-up, props 미세 조정, 명백한 typo.

## Step-Gating (중요)

4단은 *한 번에 모두 수행* 이 아니라 **각 단 사이에 사용자 게이트**. [using-cadence](../using-cadence/SKILL.md) 의 step-gating 정신:

```
1단: 컨텍스트 수집  → [📝 결과 보고] → [👤 검토] → 다음
2단: 옵션 탐색      → [📝 옵션 표 + Contrarian] → [👤 선택]   → 다음
3단: 위험/폐기/OoS  → [📝 플랜 + 위험 명시] → [👤 승인]        → 다음
4단: 외부 검증 (선택) → [📝 보조 검증 결과 + 의견] → [👤 결정]      → 끝
```

AI 는 각 단 산출물만 만들고 *보고 후 정지*. 사용자 자유 응답 후 다음 단 진행. AskUserQuestion 강요 X.

**작업 크기에 따라 단 수 조정** (using-cadence § 1-1):
- 작은 작업 → 4단 skip, 결과만 보고
- 중간 작업 → 2-3단 묶음 (예: 1+2 같이, 3+4 같이)
- 큰 작업 → 4단 mandatory, 매 단 게이트

## 1. 컨텍스트 수집 (mandatory)

플랜 작성 *전* 다음 4가지를 모두 확인한다.

### 1-1. 관련 회고 스캔

- cwd 에 `docs/retrospectives/INDEX.md` 가 있으면 카테고리 매칭으로 관련 회고 발굴
- 매칭된 회고는 본문까지 정독, takeaway 를 플랜에 반영
- 회고 50+ 건 등 규모가 크면 `Explore` subagent 에 위임 ("관련 회고를 찾아 takeaway 를 정리해줘")
- 회고 시스템이 없는 프로젝트면 git log + 기존 PR 본문 스캔으로 대체

### 1-2. 기존 컴포넌트 / 패턴 검색 (grep-miss 방지)

대표 통점: *"기존 X 컴포넌트 재사용 가능?" 을 사용자 확인 지점에 두면 grep 으로 못 찾는 자체 모듈을 한 답변으로 발견* (분산 호출 패턴은 name 검색만으로 안 잡힘).

- 프로젝트의 모듈 / 컴포넌트 디렉토리에서 유사 패턴 검색 (위치는 프로젝트마다 다름)
- **보고 / 옵션 제안에 `기존 X 재사용 가능?` 확인 지점을 포함** — 사용자 지식이 grep 보다 빠를 때 많음. 단, 특정 다지선다 도구로 묶지 말고 자유 응답을 열어둔다.

> *AST 검색 / 의존 그래프 분석 / 외부 contract 변경 감지 같은 도구별 자동화* (예: `ast-grep`, `knip`, `openapi-diff` 등) 는 *별도 stack-특화 skill repo* 또는 *프로젝트 hook* 에서 다룬다. cadence 본 repo 는 *수동 검색 절차* 만 정의.

### 1-3. 메모리 룰 cross-check

- 작업 영역의 관련 메모리 룰을 훑기 (cadence-ai-behavior 룰 + 프로젝트 L2 룰)
- 플랜이 룰과 충돌하면 *룰 우선* 또는 *룰 갱신 제안*

### 1-4. 스펙 ↔ 구현 대조 (`done` ≠ 구현 완성)

스펙시트 `status: done` 은 *그 PR 시점에 닫혔다* 는 뜻이지 *모든 분기/매핑이 코드에 반영됐다* 는 보장이 아니다. 다분기 매핑(N라벨 표 등)은 stub(예: 단일 필드만 반환)으로 닫히기 쉽다.

- **`done` 스펙 영역을 건드릴 때 spec 본문 ↔ 실제 구현 함수를 대조**한다. 스펙의 라벨/분기 표가 실제 코드에 다 있는지 해당 함수를 직접 읽는다.
- 특히 *사용자가 표시/동작 버그를 제보* 하면 "done 이니 맞겠지" 가정 말고 해당 표시·분기 함수부터 읽는다 (done stub 이 흔한 원인).
- 사례: 상태 라벨 표가 `done` 스펙에 닫혀 있는데 실제 formatter 는 raw status 만 반환하는 stub → 특정 상태에서 이전 라벨이 그대로 노출.

## 2. 옵션 탐색 (mandatory)

단일 안 갇힘은 회고에서 반복 발견되는 실패 모드 (*premature abstraction, stale spec 가정, 단일 결정 단정 톤*). 다음을 강제한다.

### 2-1. 최소 2안 제시

- 플랜에 *추천 안* + *대안 1안 이상* 명시
- 각 안의 장단점 / 비용 / 위험 비교
- 단일 안만 제출되면 **재검토** — 옵션이 정말 1개뿐인지 자문

### 2-2. Contrarian 질문 1개

플랜 작성 후 자문하고 답을 플랜에 적는다:

> "반대 가정이 사실이라면? 이 결정이 틀렸을 가능성은?"

예시:
- "spec 의 명시 endpoint 가 server contract 와 다르면?"
- "이 컴포넌트가 1곳만 쓴다고 가정했는데 grep 못 찾은 호출처가 있으면?"
- "이 추상화가 다음 PR 에서 깨질 가능성은?"

## 3. 위험 / 폐기 조건 / Out of scope (mandatory)

머지 직전 발견되는 위험은 회수 비용 크다. 플랜에 다음 3 섹션이 모두 있어야 한다:

- **위험** (≥ 1) — 알려진 미해결 의존성, 외부 contract 변경 가능성, 회귀 가능 영역
- **폐기 조건** (≥ 1) — *어떻게 알아챌까* — 이 접근이 틀렸다고 판단할 시그널
- **Out of scope** — 본 작업/PR 에서 다루지 *않을* 항목 (별도 PR / follow-up). 봇 트리아지 비용 절감

## 4. 외부 검증 — 사다리 (Verification Ladder)

Eugene Yan 의 *저렴 → 비싼* 사다리 패턴 차용. 단일 layer 가 아니라 *비용 효율적 escalation*. 실패/disagree 시만 상위 layer 진입.

### 4-layer 구조

| Layer | 비용 | 자동/조건부 | 도구 예시 |
| --- | --- | --- | --- |
| **L1. 결정론 (mechanical)** | 토큰 0 | **자동** (post-edit hook 권장) | tsc / oxlint / oxfmt / ruff / build |
| **L2. cheap semantic** | 저토큰, 1회 | **조건부 후보** (완료 보고 전 검토) | 1차 보조 AI review (스펙 정합) — [feedback_crosscheck](../cadence-ai-behavior/rules/feedback_crosscheck.md) 의 *주 도구 → 보조 도구 1* |
| **L3. consensus** | 중토큰, 조건부 | **L2 disagree / 의심 시만** | 다른 모델 family 또는 PR review bot — 다중 리뷰 경로 합의 |
| **L4. 수동 inspection** | 사람 시간 | **L3 도 미해결 시 / 핵심 결정** | 사용자 직접 판단, 독립 리뷰의 *플랜 텍스트 비판* |

### 운용 원칙

- **L1 은 항상 통과해야 다음 단계 진입** — 빨간불에서 L2 호출 금지
- **L2 가 OK 면 L3 호출 X** — *비용 효율*. L3 는 *L2 가 disagree* 또는 *사용자 명시 요청* 시만
- **L4 는 *판단 필요* 한 결정** — 도메인 추상화 / 새 컴포넌트 / 새 라우트 / contract gap 의심 시
- **각 layer 결과는 *합산이 아니라 게이트*** — L1 통과 → L2 통과 → … 순차

### 적용 시점

- **post-edit (L1)**: 매 편집 후 자동 (프로젝트의 hook / lint-staged 등)
- **작업 완료 (L1 + L2 검토)**: 기능/버그픽스 단위 완료 시 L1 은 수행, L2 는 보조 리뷰 경로가 설정되어 있거나 사용자 승인이 있을 때 실행
- **PR 머지 직전 (L1 + L2 + L3 조건부)**: 누적된 변경에 다시 한 번
- **큰 결정 (L4)**: 독립 리뷰의 *플랜 단계 비판* — cadence-plan § 3 의 위험 명시와 결합

### 작업 크기별

| 작업 크기 | 적용 layer |
| --- | --- |
| 작은 (≤ 10분) | L1 만 |
| 중간 (10–30분) | L1 + L2 (작업 완료 시) |
| 큰 (≥ 30분 / 새 도메인 / 추상화) | L1 + L2 + (조건부 L3) + L4 (플랜 단계 비판) |

이 사다리는 **단일 모델 편향 회피** ([feedback_crosscheck](../cadence-ai-behavior/rules/feedback_crosscheck.md)) 와 결합해 *비용 효율적 다각도 검증* 을 보장.

## 코딩 판단 원칙 (외부 stack-특화 skill)

플랜의 *옵션 탐색* 단계에 *흔한 단축 경로* ("단언으로 풀자 / disable 로 막자 / types.ts 만들자 / 컴포넌트 분리하자") 가 나오면 자동 재검토 게이트 작동.

이런 *코딩 판단 원칙* 은 *언어 / 프레임워크별 예시가 다르므로* cadence 본 repo 가 아닌 **별도 stack-특화 skill repo** 에서 다룬다 (예: frontend-skills / python-skills / go-skills 등). 본 repo 는 *cross-stack 범용* 만 담당.

해당 skill 이 설치되어 있으면 플랜 단계에서 동시 적용. 미설치 시 본 단축 경로 게이트만 약해질 뿐 다른 단계 작동에는 영향 없음.

## 스펙시트 작성 보조 렌즈 (lazy-load)

스펙시트는 *탐색 → 결정 → 문서화* 의 세 단계를 거친다. `cadence-plan` 은 결정권과 게이트를 담당하고, 외부 helper skill 은 필요한 순간에만 보조 렌즈로 로드한다. helper 가 설치되어 있지 않으면 아래 체크리스트를 본 skill 안에서 직접 수행한다.

| 렌즈 | 로드 시점 | 역할 | 금지 |
| --- | --- | --- | --- |
| **Brainstorming Lens** (`brainstorming`, superpowers 계열 등) | 요구가 모호하거나 첫 문제 정의 단계 | 가능한 해석 2-3개, 가장 작은 첫 PR 단위, 확인 질문 후보, 반대 가정 도출 | 바로 스펙시트 확정 / 구현 진입 |
| **Writing Lens** (`writing-skills`, `clarify` 등) | 결정된 내용을 스펙시트로 정리할 때 | 구현 가능한 명세로 재구성, facts / assumptions / TBD 분리, 읽기 쉬운 섹션화 | 아직 결정 안 된 가정을 매끈한 문장으로 확정처럼 포장 |
| **Hardening Lens** (`harden`, `audit`, stack 특화 skill 등) | `ready` 전 또는 위험 큰 UI/API 흐름 | 실패 UI, edge case, 접근성, i18n, responsive, contract gap 체크 | 본 PR 범위를 몰래 확장 |

### 운용 원칙

- **Lazy-load**: 모든 스펙시트에 helper 를 자동 로드하지 않는다. 요구가 명확한 중간 작업은 cadence-plan 축약형만으로 충분하다.
- **Decision before Writing**: writing 계열은 formatter/editor 이지 decision maker 가 아니다. 결정은 옵션 탐색 + 사용자 게이트에서 끝낸 뒤 문서화한다.
- **TBD 보존**: 불확실한 항목은 문장으로 숨기지 말고 `## TBD`, `## 위험 / 폐기 조건`, `## Out of scope` 에 남긴다.
- **자동 chain 금지**: Brainstorming → Plan → Writing → 구현을 한 turn 에 자동으로 이어가지 않는다. 스펙 초안 보고 후 사용자 게이트를 둔다.

## 산출물 형식 — 스펙시트 메타-구조

4단 mandatory 의 *결과물* 은 **스펙시트 (specsheet)** 형식으로 결정화한다. 도구/도메인 무관 *작업 단위 문서화 원칙*. 프로젝트별 구체 어휘는 *프로젝트 안 `_template.md`* 가 담당하고, 본 skill 은 **메타-구조** 만 정의.

### 4단 → 스펙시트 매핑

| 플랜 단 | 산출물 위치 (스펙시트 섹션) |
| --- | --- |
| **1단. 컨텍스트 수집** | `## 개요`, `## 동작 / 변경 목록`, `## 관련 회고` link |
| **2단. 옵션 + Contrarian** | `## 동작 상세`, `## 엣지 케이스` |
| **3단. 위험 / 폐기 / Out of scope** | `## TBD`, `## 후속 작업 (별도 작업)`, `## 위험` |
| **4단. 외부 검증** | `## 검증 결과` (보조 도구 의견 요약), `## 구현 체크리스트` 확정 |

### 스펙시트 메타-구조 (필수 섹션)

```markdown
---
title: <한 줄 제목>
status: draft | ready | in-progress | done | revised
created: YYYY-MM-DD
updated: YYYY-MM-DD
related-retrospectives: [<link>, ...]
---

## 개요
<목표 1-2 문장 — 왜 이 작업을 하는가>

## 동작 / 변경 목록
- [ ] <동작 1>
- [ ] <동작 2>

## 동작 상세
### <동작 1>
- 사용자 흐름 / 입력 → 출력 / 에러 처리

## 공통 사항
- 진입 조건 / 이탈 동작 / 상태 흐름

## 엣지 케이스
- <Contrarian 질문 결과>

## TBD
- <해소 안 된 결정 — 모두 해소되면 status: ready>

## 위험 / 폐기 조건
- 위험: <≥ 1>
- 폐기 조건: <어떻게 알아챌까>

## Out of scope
- <본 작업에서 다루지 않을 항목>

## 구현 체크리스트
- [ ] <100% 시 status: done>

## 후속 작업 (별도 PR)
- [ ] <- PR #N>

## 관련 회고
- [<link to retrospective>]
```

### lifecycle (선택 — 프로젝트가 정착 운용 시)

프로젝트가 디렉토리 lifecycle 을 운용하면 본 skill 은 그 컨벤션 따름:

| status | 위치 (예시) |
| --- | --- |
| draft / ready | `backlog/` |
| in-progress | `in-progress/` |
| done / revised | `done/` |

위는 예시 — 각 프로젝트는 자기 lifecycle 따름.

### 작업 크기와 스펙시트

| 작업 크기 | 스펙시트 |
| --- | --- |
| 작은 (≤ 10분) | 스펙시트 생략 가능. PR 본문에 *개요 + 변경 목록* 만 |
| 중간 (10–30분) | 스펙시트 권장. 모든 섹션 작성하되 *얇게* |
| 큰 (≥ 30분) | 스펙시트 mandatory. 모든 섹션 *상세* |

### 회고와의 연결

작업 완료 후 *학습할 점* 이 있으면 [cadence-retrospective](../cadence-retrospective/SKILL.md) 트리거. 스펙시트의 `## 관련 회고` 섹션이 *역방향 link* — 회고가 어떤 스펙시트에서 나왔는지 추적 가능.

## 위반 시 결과

- 1번 (컨텍스트 수집) 누락 → **플랜 재작성**. 회고 / 기존 컴포넌트 검색 누락은 단순 누락이 아니라 *반복 비용 발생원*
- 2번 (옵션 1안만 제출) → 사용자가 "다른 옵션은?" 묻기 전 자체 보완
- 3번 (위험 / 폐기 / Out of scope 누락) → 머지 직전 회수 비용 위험

## 프로젝트별 적용 (Layer 분리)

본 skill 은 *프로세스* 만 정의. 룰 내용은 cwd 에서 동적 스캔:
- L2 (프로젝트 기술 컨벤션) — cwd 의 `docs/ai-rules/`, root config, 또는 동등 위치
- L3 (프로젝트 도메인 결정) — cwd 의 메모리, `docs/specsheets/done/` 등

회고 / 스펙시트 구조가 정착된 프로젝트는 그 자산을 동적 활용. 회고가 없는 프로젝트는 git log + 기존 PR 로 대체.

## 발동 시 사용자 시그널

본 skill 작동 중 AI 응답에 다음 패턴:

- 작업 시작 시 *"이건 [작은/중간/큰] 작업으로 보입니다, N step 으로 진행"* — 작업 크기 판정
- 큰 작업 시 *"## Step N/4 — <단계명>"* — 4단 mandatory
- 옵션 탐색 시 *"옵션 A / B / C"* + *"Contrarian: 반대 가정이 사실이라면? ..."* — § 2 옵션 2 안
- *"위험: ..."* / *"폐기 조건: ..."* / *"Out of scope: ..."* — § 3 mandatory
- 외부 검증 시 *"L1 mechanical 통과 → L2 보조 review → L3 consensus (조건부) → L4 manual"* — § 4 검증 사다리
- 스펙시트 초안 작성 시 *"Brainstorming Lens / Writing Lens"* 를 명시하되, 설치된 helper 가 없으면 본문 체크리스트로 대체
- 산출물이 *스펙시트 메타-구조* 로 결정화 (개요 / 동작 목록 / 엣지 케이스 / TBD / 구현 체크리스트 / 후속 작업 / 관련 회고)
- 추상화 결정 시 "단언으로 풀자 / disable 로 막자 / types.ts 만들자 / 컴포넌트 분리하자" → 자동 재검토 (stack-특화 skill 설치 시)

미작동 시 → [USAGE.md § 4 진단표](../../USAGE.md) 참조.

## 관련

- [cadence-ai-behavior](../cadence-ai-behavior/SKILL.md) — AI 행동 통제 룰
- [cadence-retrospective](../cadence-retrospective/SKILL.md) — 작업 완료/실패 후 회고 작성 가이드
- [using-cadence](../using-cadence/SKILL.md) — 메타 라우팅 + step-gating
- [USAGE.md](../../USAGE.md) — 시나리오별 사용 예시
- 프로젝트의 `docs/retrospectives/INDEX.md` — 회고 스캔 entry point (있는 경우)
