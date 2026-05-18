---
name: cadence-code-principles
description: 작성자의 *개인 코딩 판단 원칙* 4가지 — 타입 단언 금지, 린트 disable 주석 지양, 타입 co-location, 재사용 전까지 인라인 유지 (YAGNI). 객관적 일반 원칙처럼 보이지만 *예외 폭 / 적용 기준* 이 개인 선호. fork 자가 자기 선호로 수정 또는 *옵션 skip* 가능. 도구·도메인 무관.
---

# cadence-code-principles

작성자의 **개인 코딩 판단 원칙** 4가지. *린터 강제 가능한 취향* (괄호 / 배열 숏폼 등) 과 *AI 행동 통제* (sycophancy / 자동 push 등) 의 *중간 영역* — 판단 룰이라 자동화 어렵고, 그렇다고 AI 만의 룰도 아님.

## 왜 별도 skill 인가

이 4가지는 **객관적 일반 원칙처럼 보이지만 사실 *예외 폭 / 적용 기준* 이 개인적**:

- "타입 단언 금지" — 일반적이지만 *어디까지 예외 인정할지* 가 사람마다 다름
- "타입 co-location" — *types.ts 별도 선호* 하는 개발자도 다수
- "인라인 유지 (YAGNI)" — *언제 추상화* 가 적정한지 판단 기준이 개인적
- "린트 disable 지양" — 일반적이지만 *언제 예외 인정* 이 개인적

따라서 fork 자가 *자기 선호로 수정* 하거나 *옵션 skip* 할 수 있도록 별도 skill 로 분리. cadence 의 다른 skill (ai-behavior / plan / retrospective) 은 *AI 협업 구조* 자체라 fork 시 보존 권장이지만, *본 skill 은 선택* 사항.

## 룰 4건

전부 [rules/](./rules/) 디렉토리 안의 frontmatter 파일로 관리:

1. [타입 단언(as) 금지](./rules/feedback_no_type_assertions.md) — 스키마 / type guard / 자료구조 재설계로 회피
2. [린트 disable 주석 지양](./rules/feedback_no_lint_disable_comments.md) — 구조 변경으로 원인 제거
3. [타입 co-location](./rules/feedback_type_colocation.md) — 사용처 가까이, types.ts 는 3+ 공유 시만
4. [재사용 전까지 인라인 유지](./rules/feedback_inline_until_reused.md) — 5–10줄 래퍼는 호출 모듈 안 내부 함수, 분리는 구체적 근거 필요

## 적용 시점

- **코드 작성 / 추상화 결정** 시 — 본 4 원칙 자동 적용
- **플랜 단계** ([cadence-plan](../cadence-plan/SKILL.md)) 의 옵션 탐색에서 "단언으로 풀자 / disable 로 막자 / types.ts 만들자 / 컴포넌트 분리하자" 같은 *단축 경로* 가 나오면 본 원칙 게이트로 자동 재검토

## 설치

```bash
~/Repository/cadence/cadence-code-principles/install.sh
```

cwd 의 `~/.claude/projects/<encoded-cwd>/memory/` 에 4 룰 파일 복사 + `MEMORY.md` 인덱스에 sentinel marker 영역 갱신.

## fork 자 가이드

본 skill 은 *개인 선호* 라 fork 시 다음 중 하나:

- **그대로 사용** — 작성자 판단에 동의
- **수정 후 사용** — 자기 선호로 룰 본문 갱신 (예: types.ts 별도 선호면 type_colocation 룰 반대로)
- **Skip** — symlink 안 걸고 install.sh 도 실행 안 함. 다른 cadence-* skill 은 그대로 사용 가능

## 발동 시 사용자 시그널

본 skill 작동 중 AI 응답에 다음 패턴:

- 추상화 결정 시 *"단언으로 풀자 / disable 로 막자 / types.ts 만들자 / 컴포넌트 분리하자"* 같은 단축 경로가 나오면 → 자동 재검토 게이트
- "이 단언은 자료구조 결함 신호 → 스키마 / type guard / 재설계로 회피 검토"
- "disable 주석 대신 구조 변경 옵션: ..."
- "types.ts 신설 전 *실제 공유처 수* 점검 — 3+ 이면 신설, 미만이면 co-locate"
- "이 컴포넌트 분리는 *재사용처 ≥ 2 + 자체 state / 테스트 경계* 중 어느 것?" → 근거 없으면 인라인 유지

미작동 시 → [USAGE.md § 4 진단표](../USAGE.md) 참조.

## 관련

- [cadence-plan](../cadence-plan/SKILL.md) — 플랜 단계의 옵션 탐색에서 본 원칙 게이트
- [cadence-ai-behavior](../cadence-ai-behavior/SKILL.md) — AI 행동 통제 (본 skill 과 결 다름)
- [USAGE.md](../USAGE.md) — 시나리오별 사용 예시
