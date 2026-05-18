---
name: cadence-retrospective
description: 개인 회고 작성·관리 skill. 작업 완료 / 실패 / mid-PR 학습 / 룰 위반 발견 시 트리거. 한 줄 takeaway INDEX + 본문 (무엇/왜/해결/예방) 메타-구조. recurring 패턴은 룰화 승급 검토. 도구·도메인 무관 (프로젝트별 회고 어휘는 cwd 동적 스캔).
---

# cadence-retrospective

개인 회고 작성·관리 skill. *작업 사이클의 학습 단계* 를 책임진다. [cadence-plan](../cadence-plan/SKILL.md) 이 *진입 단계* 라면 본 skill 은 *완료 단계* — 두 skill 이 *룰 진화 루프* 의 양 끝.

## 트리거

다음 시점 중 하나에 회고 작성을 *검토* (강제 X — 사용자 결정 따름):

| 트리거 | 회고 가치 |
| --- | --- |
| **작업 완료** (PR 머지 직후) | 워크플로우 / 도구 / 협업 패턴에서 *예상과 다른 점* 이 있었나? |
| **작업 실패 / 회수** (revert / 큰 재작업) | *근본 원인* 추출 — 다음 작업에 재발 방지 |
| **mid-PR 학습** (스펙 / yaml / 외부 contract 변경) | spec drift / contract gap 같은 *반복 빈도 높은* 패턴 |
| **봇 리뷰 합의 거부** (codex / gemini / coderabbit 합의를 거부) | 합의 ≠ 정답 의 *근거 기록* |
| **룰 위반 발견** (기존 룰을 무심코 어김) | 룰 자체의 *명문화 부족* 또는 *예외 케이스* 신호 |
| **사용자 명시 요청** ("이건 회고 쓰자") | 사용자 학습 가치 판단 |
| **트랜스크립트 마이닝 신호** (passive — 아래 § 트랜스크립트 마이닝 참조) | *조용한 실패* — 명시 사건 X, 사용자 발화 패턴이 룰 갭을 드러냄 |

**제외**: 1줄 fix, 명백한 typo, 외부 패키지 업그레이드만 한 PR — 회고 생략. 회고도 *작은 작업까지 강제하면 cadence 깨짐*.

## 트랜스크립트 마이닝 (passive 신호)

명시 사건 (실패 / 합의 거부 / 룰 위반) 은 *눈에 띄는* 통점만 잡는다. **사용자 발화 패턴** 이 *조용한 실패* — 룰 갭이지만 명시 사건으로 안 드러나는 영역을 보여준다.

Eugene Yan 의 [Working with AI](https://eugeneyan.com/writing/working-with-ai/) 의 트랜스크립트 마이닝 패턴을 차용.

### 신호 패턴 (사용자 발화 빈도)

| 패턴 | 의미 |
| --- | --- |
| "X 도 확인했어?" / "Y 도 해줘" / "그것도 같이" — **follow-up 빈도** | cadence-plan § 1 *컨텍스트 수집* 갭 — AI 가 처음에 누락 |
| "여전히 틀렸어" / "또 같은 실수" — **재발 표현** | 기존 룰을 무심코 어김 — 룰 자체 명문화 약함 |
| "그게 아니라" / "다시 해줘" / "내가 말한건…" — **redirect 빈도** | cadence-plan § 2 *옵션 탐색* 부족 — AI 가 단일 안 강요 |
| "왜 그렇게 했어?" / "이유는?" — **설명 요청 빈도** | AI 의 *결정 근거* 명시 부족 |
| "그냥 진행해" / "묻지 말고" — **over-asking 신호** | using-cadence § 7-2 *AskUserQuestion 강요 함정* 발현 |

### 운용 절차

1. **주기**: 주 1회 또는 작업 사이클 종료 시 (PR 머지 후 회고 단계와 결합)
2. **분석 단위**: 최근 N 턴의 사용자 메시지만 (AI 응답 제외) — `transcript_path` 의 JSONL 활용
3. **빈도 임계**: 같은 패턴이 *3+ 회* 반복되면 *룰 갭 후보*
4. **출력**: 발견된 패턴 + 빈도 + 후보 룰화 결로 분류 (cadence-ai-behavior / cadence-plan / 프로젝트 ai-rules)
5. **사용자 보고 → 합의 → 회고 또는 룰 추가** (자동 X)

### 도구

- 현재 세션: `transcript_path` (UserPromptSubmit hook context) 의 JSONL 파일 grep
- 과거 세션: `~/.claude/projects/<encoded>/<session-id>.jsonl` 다수 grep — `jq` 또는 `grep` 으로 사용자 메시지만 추출

```bash
# 예: 최근 5 세션의 사용자 메시지에서 "다시" / "틀렸" 빈도
grep -h '"role":"user"' ~/.claude/projects/<encoded>/*.jsonl | \
  grep -oE '다시|틀렸|아니라|또 같은' | sort | uniq -c | sort -rn
```

### 한계 / 함정

- 트랜스크립트 마이닝은 *passive 사후 분석* — *실시간* 룰 적용은 cadence-ai-behavior 의 자동 발동에 맡김
- 발화 패턴만으로 *근본 원인* 단정 X — *후보 신호* 로만 사용. 회고 본문에서 근본 원인 검증
- 사용자 발화 자체가 *룰* 의 형태일 수도 ("그러니까 다음에는 X 하자") — 이 경우 *명시 사건* 으로 분류, 마이닝 대상 X

## 메타-구조 (도구·도메인 무관)

```markdown
---
title: <YYYY-MM-DD-주제-한줄>
date: YYYY-MM-DD
related-specs: [<spec link>, ...]
related-rules: [<rule link>, ...]
status: draft | published
---

# <한 줄 takeaway — INDEX 에 표시될 형태>

## 무엇이 일어났나
<관찰 가능한 사실 — 코드 / 행동 / 결과>

## 왜 일어났나 (근본 원인)
<5 whys 패턴 권장. 표면 원인 X, 근본 원인 1-3개>

## 어떻게 해결했나
<실제 수정 / 회피 / 결정 — 코드 인용 또는 PR link>

## 다음에 어떻게 예방?
<recurring 패턴 가능성 / 룰화 가치 / 체크리스트 추가>

## 룰화 승급 검토 (선택)
이 회고가 *recurring 패턴* 이라고 판단되면 다음 중 하나로 승급:
- [ ] cadence-ai-behavior 룰 추가 — AI 행동 통제 결
- [ ] cadence-plan 룰 추가 — 플랜 단계 결
- [ ] 프로젝트별 ai-rules 추가 — 프로젝트 종속 결
- [ ] 룰화 불필요 — 1회성 또는 컨텍스트 의존
```

## 한 줄 takeaway 원칙

회고의 *제목* 또는 *첫 줄* 은 INDEX 에 등재될 *한 줄 takeaway*. 다음 패턴:

❌ "주문 페이지 작업 회고" (정보 0)<br>
✅ "주문 SDK contract 가설은 generated SDK 로 검증 필수 — 같은 URL 도 메서드/응답 타입에 따라 의미 다름"

한 줄로 *교훈* 이 드러나야 함. 카테고리 매칭에도 유리.

## INDEX 관리

프로젝트에 회고 디렉토리 (`docs/retrospectives/` 또는 동등) 가 있으면 **INDEX.md** 를 카테고리별로 운용:

```markdown
# 회고 인덱스

## 라우팅 / 가드 / 레이아웃
- [<file>](.) — <한 줄 takeaway>

## 데이터 페칭 / Suspense / 쿼리 경계
- [<file>](.) — <한 줄 takeaway>

## 폼 / 검증 / 인증

## 리뷰 프로세스 / 협업

## 스펙 / 계획 / 추상화 판단

## UI 패턴 / 컨테이너 쿼리 / 모달

## 프리미티브 / 마이그레이션

## 모바일 / 네이티브 SDK / 플러그인
```

**카테고리는 프로젝트 색** — 위는 예시. 각 프로젝트는 자기 도메인에 맞는 카테고리.

## 회고 작성 시점 절차 (step-gating)

```
1. 트리거 발생 → AI 가 회고 가치 평가 ("이 작업에서 학습할 점이 있는가?")
2. AI 가 회고 *초안* 생성 → [📝 보고]
3. [👤 검토 / 수정 / "회고 불필요"]
4. 합의 시 회고 파일 생성 + INDEX 갱신 → [📝 보고]
5. [👤 룰화 승급 결정]
6. 합의 시 새 룰 추가 (cadence-ai-behavior / cadence-plan / 프로젝트 ai-rules)
```

AI 가 *자동으로* 회고 파일 생성 X — 사용자 합의 후. [feedback_no_auto_commit_push](../cadence-ai-behavior/rules/feedback_no_auto_commit_push.md) 와 같은 결.

## 룰화 승급 조건

회고를 *룰* 로 승급할 때 다음 점검:

- [ ] **재발 가능성** — *recurring* 패턴인가? 1회성이면 회고로만 남기고 룰 X
- [ ] **AI 행동 통제 vs 프로젝트 컨벤션 vs 일반 원칙** — 어느 layer 인지 명확
- [ ] **도구/도메인 무관성** — 도구 일반? 프로젝트 종속? ([cadence/README.md § 룰 작성 가이드](../README.md))
- [ ] **이미 있는 룰과 중복** 확인 — consolidate-memory 스킬과 함께 점검

## 부트스트래핑 패턴 (skill 자체 진화)

회고가 *recurring 패턴* 이라 판단되어 *룰* 이 아닌 *skill* 단위로 묶일 가치가 있을 때, **AI 가 자기 자신을 skill 화** 하는 메타-패턴. Eugene Yan 의 부트스트래핑 차용.

### 절차

1. **1차 작업 수행 (skill 없음)** — 사용자와 AI 가 함께 작업, 시행착오 포함
2. **사용자 또는 AI 가 "이걸 skill 로 만들자" 제안** — 트리거: 같은 패턴 작업 *2-3 회 반복* 시
3. **AI 가 `SKILL.md` 초안 생성** — 트랜스크립트의 *before / after* 쌍을 직접 인용 → 보고
4. **사용자 검토 + 합의** — 부족한 점 / 빠진 단계 / 과잉 단계 지적
5. **다음 같은 작업에서 *드래프트 skill* 적용 실행** — 실시간 검증
6. **피드백 → skill 갱신** — 트랜스크립트의 새 신호로 SKILL.md 다듬기
7. *(반복)* 새 트리거 발생 시 또 갱신

### 핵심 — 트랜스크립트가 base

부트스트래핑의 *진실원천* 은 *과거 트랜스크립트의 before / after 쌍*. AI 가 *추상화 먼저 하지 말 것* — 실제 수행한 행동의 *명령형* 절차부터 적되, 점차 *원칙* 으로 일반화.

### 안티-패턴

- **첫 시도부터 완벽한 SKILL.md** 생성 시도 → 추상화 과잉, 실제 동작과 어긋남
- **사용자 합의 없이 자동 skill 생성** → [feedback_no_auto_commit_push](../cadence-ai-behavior/rules/feedback_no_auto_commit_push.md) 와 같은 결, 명시 요청 후만
- **skill 화 후 트랜스크립트 마이닝 중단** → 갱신 사이클 끊김. *지속적* 마이닝 필수

### 본 skill 자체의 부트스트래핑

본 cadence-retrospective 도 이 패턴으로 진화 — 향후 회고 작성 시 발견된 *빠진 단계* 가 본 SKILL.md 갱신의 입력.

## 회고와 [cadence-plan](../cadence-plan/SKILL.md) 의 연결

| 시점 | cadence-plan | cadence-retrospective |
| --- | --- | --- |
| 진입 | 1-1 *회고 스캔* — INDEX 카테고리 매칭 | (관련 회고 *조회* 대상) |
| 진행 | 4단 mandatory | — |
| 산출물 | 스펙시트 (`## 관련 회고` link 포함) | — |
| 완료 | — | 회고 작성 검토 → INDEX 등재 |
| 사이클 | (룰 위반 발견 시) | 룰화 승급 → cadence-ai-behavior / plan 갱신 |

회고 → 룰 → 다음 플랜의 *컨텍스트 수집* 에서 자동 참조 → 다음 회고 → … *학습 루프*.

## 프로젝트별 적용

- 회고 디렉토리 위치 (`docs/retrospectives/` 또는 동등) — 프로젝트 선택
- 카테고리 어휘 — 프로젝트 도메인
- INDEX 작성 빈도 — 매 회고 시 1줄 추가 (룰)

본 skill 은 *메타-구조 + 운용 절차* 만 정의. 구체 컨벤션은 프로젝트 안.

## 발동 시 사용자 시그널

본 skill 작동 중 AI 응답에 다음 패턴:

- 작업 완료 / 실패 / mid-PR 학습 시점에 *"회고 가치 평가: ..."* — 가치 있으면 *초안 제안*
- 회고 본문이 *메타-구조* (무엇이 / 왜 / 어떻게 해결 / 어떻게 예방) 로 결정화
- 한 줄 takeaway 가 *제목 또는 첫 줄* 로 — INDEX 등재 가능 형태
- recurring 패턴 발견 시 *"룰화 승급 검토: ai-behavior / plan / 프로젝트 ai-rules 중 어느 layer?"*
- 트랜스크립트 마이닝 시점 (주 1회 / 작업 사이클 종료 시) *"최근 사용자 발화 패턴 분석: '다시' / '또 같은' / '아니라' 3+ 회 — 룰 갭 후보"*
- 부트스트래핑 시 *"이걸 skill 로 만들자, 초안: ..."*

미작동 시 → [USAGE.md § 4 진단표](../USAGE.md) 참조.

## 관련

- [cadence-plan](../cadence-plan/SKILL.md) — 작업 진입 단계, 회고 *조회* 측
- [cadence-ai-behavior](../cadence-ai-behavior/SKILL.md) — 룰화 승급 대상 1
- [using-cadence](../using-cadence/SKILL.md) — 트리거 라우팅
- [cadence/README.md § 룰 작성 가이드](../README.md) — 룰화 시 점검 패턴
- [USAGE.md](../USAGE.md) — 시나리오별 사용 예시
