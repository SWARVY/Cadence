---
name: cadence-ai-behavior
description: Claude/AI 행동 통제 룰 7개. AI 가 가지는 특유의 경향(sycophancy, 즉시 편집, 자동 push, 장황한 주석, 경로 혼동 등)을 의도적으로 통제한다. 사람-사람 협업에는 무관하며 AI 도구 사용 시점에만 의미가 있다. 프로젝트와 무관 (technology-agnostic).
---

# cadence-ai-behavior

사용자가 Claude (또는 다른 AI 코딩 도구) 와 협업할 때 *AI 의 행동을 의도적으로 통제* 하는 룰 모음. 사람 협업자에게는 무의미하므로 일반 코딩 가이드와 분리.

## 적용 시점

- AI 가 응답 생성하는 *모든 turn* — 행동/태도/리뷰 응답/편집 결정
- 도구 호출 결정 (commit / push / PR / codex 등)
- 사용자 피드백 처리 (즉시 편집 vs 견해 교환 결정)

## 룰 7개

### AI 의 *상호작용 경향* 통제 (2건)

1. [사용자 의견 = 검토 대상](./rules/feedback_collaborator_not_authority.md)
   - AI 의 sycophancy (반사적 동의) 통제
   - 사용자 의견은 "의견" 으로 검토, "진실" 로 수용 X
   - 더 나은 안이 있으면 질문이 아닌 *주장* 으로 즉시 표명
2. [리뷰는 대화 오프너](./rules/feedback_review_as_dialogue.md)
   - AI 가 코드 리뷰/피드백 받자마자 편집 시작하는 경향 통제
   - 확인형 질문도 대화 오프너 — "맞을까?", "없지?" 등은 현 상태 확인이지 수정 지시 X
   - 부분 확인 ≠ 실행 승인

### AI 의 *실행 경향* 통제 (2건)

3. [원격 반영은 명시 요청 시에만](./rules/feedback_no_auto_commit_push.md)
   - AI 가 워크플로우 끝에서 자동으로 commit / push / PR 까지 이어가는 경향 통제
   - 한 PR 사이클 내 한 번의 push 요청을 후속 변경까지 일반화 금지
4. [워크트리 절대 경로](./rules/feedback_worktree_absolute_paths.md)
   - AI 가 워크트리 환경에서 절대 경로를 메인 레포로 향하게 하는 경향 통제

### AI 의 *생성 경향* 통제 (1건)

5. [주석 간결](./rules/feedback_concise_comments.md)
   - AI 가 다단 JSDoc / 절차 나열 / 자명 코드 한국어 재기술하는 경향 통제
   - 비-자명한 의도/이유만 한두 줄

### AI 도구 *통합* 룰 (2건)

6. [고추론·고비용 ↔ 저비용·실행 모델 분리](./rules/feedback_model_strategy.md)
   - 비싼 모델은 계획/분석, 저렴한 모델은 실행/반복 — 토큰 비용 최적화
   - 도구별 매핑 부속 예시 (Claude: Opus↔Sonnet / codex: GPT-5↔GPT-4o-mini / Gemini: Pro↔Flash)
   - **자체 caveat**: 저비용 모델 인계 시 룰 유지 약함 — 옵션 제시이지 강제 X
7. [주 도구 ↔ 보조 도구 크로스 체크](./rules/feedback_codex_crosscheck.md)
   - 단일 모델 편향 회피 — 다른 AI 도구로 독립 검증 (매트릭스 양방향)
   - 기능 완료 시점 자동 호출 + 명시 요청 시
   - 결과 처리는 요약 + 내 의견 (동의/반대/보류)

## 의도적으로 *제외* 된 범주

- **개인 코딩 습관** (`brace_style`, `array_shorthand`, `type_vs_interface`, `avoid_switch_case`, `top_down_ordering`) — 사람·AI 무관, 취향. linter config (`.oxlintrc.json` 등) 로 강제하는 것이 정답
- **일반 코딩 원칙** (`no_type_assertions`, `no_lint_disable_comments`, `type_colocation`, `inline_until_reused`) — AI 한정이 아닌 보편적 원칙. cadence-plan 의 *원칙* 섹션 또는 프로젝트 docs 에서 다룸
- **프로젝트 기술 컨벤션 (L2)** — 각 프로젝트의 `docs/ai-rules/` / `CLAUDE.md` / 메모리에 잔류

## 설치

```bash
~/Repository/cadence/cadence-ai-behavior/install.sh
```

cwd 의 `~/.claude/projects/<encoded-cwd>/memory/` 에 7개 룰 파일을 복사하고 `MEMORY.md` 인덱스에 sentinel marker 영역을 갱신/추가한다. 기존 동명 파일은 `--force` 없이는 skip.

## 운용 원칙

- 룰 수정: 본 repo 의 `rules/*.md` 수정 → 각 프로젝트에서 `install.sh` 재실행
- 새 룰 추가: AI 행동 통제 범주에 정확히 맞을 때만. 개인 습관/일반 원칙은 다른 위치로
- 사용자 명시 *없이도* 매 turn 자동 적용되어야 하는 룰만 본 skill 에 포함. 상황 트리거 룰은 cadence-plan 으로

## 발동 시 사용자 시그널

본 skill 작동 중 AI 응답에 다음 패턴:

- 사용자 의견 받으면 *"제안 검토: ... / 동의 / 반대: ..."* — 즉시 편집 X (review_as_dialogue + collaborator_not_authority)
- 반대 시 *주장* 으로 표명 — "제가 보기엔 B 가 낫다고 봐요, 이유는 ..."
- commit / push / PR 결정 시 *명시 요청 확인* 또는 진행 안 함 (no_auto_commit_push)
- 기능 완료 시점 *보조 도구 크로스 체크 + 결과 요약 + 의견* (codex_crosscheck)
- 주석은 *한두 줄 의도만* — 다단 JSDoc X (concise_comments)
- 워크트리 환경에서 절대 경로 `.claude/worktrees/<name>/...` 또는 도구별 워크트리 경로 (worktree_absolute_paths)

미작동 시 → [USAGE.md § 4 진단표](../USAGE.md) 참조.

## 관련

- [cadence-plan](../cadence-plan/SKILL.md) — 플랜 단계 mandatory 체크리스트 + 일반 코딩 원칙
- [USAGE.md](../USAGE.md) — 시나리오별 사용 예시
