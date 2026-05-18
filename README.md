# cadence

개인 AI 협업 skill 모음. **Cross-agent 개방 표준 (SKILL.md)** 기반 — Claude Code / OpenAI Codex / GitHub Copilot / Cursor / Windsurf / Cline / Roo Code / Gemini CLI 등 **20+ 도구에서 동일 native 작동**. 프로젝트와 무관하게 머신 단위로 설치하여 일관된 AI 협업 워크플로우를 적용한다.

> SKILL.md 는 2025-12 부터 *cross-agent 표준* 으로 자리잡음. cadence/cadence-\*/SKILL.md 는 모든 호환 도구에서 그대로 작동. 도구별 *미세 차이* (skill 디렉토리 위치 / 메모리 시스템 / session-start hook) 는 [using-cadence/SKILL.md § 7-4](./using-cadence/SKILL.md) 참조.

## 설계 원칙: 룰의 3가지 결 분리

룰은 정체에 따라 *다른 위치* 에 둔다 — 모두 한 skill 에 모으면 관리 단위가 흐려진다.

| 분류 | 정체 | 위치 |
| --- | --- | --- |
| **A. AI 행동 통제** | sycophancy, 즉시 편집, 자동 push 등 *AI 특유 경향* 통제. 사람-사람 협업 무관 | 본 repo 의 [cadence-ai-behavior](./cadence-ai-behavior/SKILL.md) |
| **A'. AI 작업 프로세스** | plan 모드 진입, 신규 spec 작성 시 mandatory 체크리스트 | 본 repo 의 [cadence-plan](./cadence-plan/SKILL.md) |
| **B. 개인 코딩 습관** | 괄호 / 배열 숏폼 / type vs interface 등 *취향* | 각 프로젝트의 **linter config** (`.oxlintrc.json` / `.eslintrc` 등) |
| **C. 개인 코딩 판단 원칙** | 단언 금지 / disable 주석 지양 / 인라인 우선 / 타입 co-location 등 — *예외 폭 / 적용 기준이 개인적* | 본 repo 의 [cadence-code-principles](./cadence-code-principles/SKILL.md) (옵션 설치) |
| **L2. 프로젝트 기술 컨벤션** | React 버전 / 폼 검증 / 디자인 토큰 / 디렉토리 구조 등 *프로젝트 종속* | 각 프로젝트의 `docs/ai-rules/` · `CLAUDE.md` · 프로젝트 메모리 |
| **L3. 프로젝트 도메인 결정** | 특정 화면/도메인의 의사결정 (예: 검색 아이콘 미포함) | 각 프로젝트 메모리 |

본 repo 는 **A + A' (필수) + C (옵션)** 를 담는다. B/L2/L3 는 본 repo 밖에 산다.

## Skill 목록

| Skill | 담당 | 적용 시점 | 필수 / 옵션 |
| --- | --- | --- | --- |
| [using-cadence](./using-cadence/SKILL.md) | **메타-skill 오케스트레이터** (라우팅 + 우선순위 + step-gating) | 매 turn 첫 점검 | 필수 |
| [cadence-ai-behavior](./cadence-ai-behavior/SKILL.md) | AI 행동 통제 7 룰 | 모든 AI 응답 turn | 필수 |
| [cadence-plan](./cadence-plan/SKILL.md) | 플랜 프로세스 4단 + 스펙시트 메타-구조 + 검증 사다리 | plan 모드, 신규 spec, 모호 작업, 추상화 결정 | 필수 |
| [cadence-retrospective](./cadence-retrospective/SKILL.md) | 회고 작성·관리, 룰화 승급 검토, 트랜스크립트 마이닝 | 작업 완료 / 실패 / mid-PR 학습 / 룰 위반 발견 | 필수 |
| [cadence-code-principles](./cadence-code-principles/SKILL.md) | 개인 코딩 판단 원칙 4건 (단언 / disable / co-location / YAGNI) | 코드 작성 / 추상화 결정 | **옵션** (개인 선호, fork 자가 skip 가능) |

**작업 사이클 루프**:
```
cadence-plan (진입)  →  실행  →  cadence-retrospective (학습)
       ↑                                    │
       └─── 룰화 승급 → cadence-ai-behavior ←┘
```

`using-cadence` 가 [obra/superpowers](https://github.com/obra/superpowers) 의 *Using Superpowers* 패턴을 *부분* 차용한 라우터. 매 turn 시작 시 *어느 sub-skill 이 발동되는지* 결정한다.

**핵심 철학**: full-ai-driven 자동 chain 거부. *AI 는 한 스텝 산출물만 만들고 보고 후 정지, 개발자 피드백 후 다음 스텝.* superpowers 의 *자동 phase chain* (TDD → review → 마감 자동) 은 차용 X.

자세한 라우팅 표 / 우선순위 / step-gating 사이클은 [using-cadence/SKILL.md](./using-cadence/SKILL.md) 참조.

## 설치

### 도구별 skill 디렉토리에 symlink

각 도구의 *공식 skill 디렉토리* 에 cadence-\* 4-5 skill 모두 symlink. 한 번 걸어두면 모든 호환 도구가 자동 매칭.

```bash
# Claude Code
mkdir -p ~/.claude/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective cadence-code-principles; do
  ln -s ~/Repository/cadence/$s ~/.claude/skills/$s
done

# OpenAI Codex (default: ~/.codex/skills, override CODEX_HOME 가능)
mkdir -p ~/.codex/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective cadence-code-principles; do
  ln -s ~/Repository/cadence/$s ~/.codex/skills/$s
done

# Windsurf / cross-agent default (도구가 인식하면 자동 동기화)
mkdir -p ~/.agents/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective cadence-code-principles; do
  ln -s ~/Repository/cadence/$s ~/.agents/skills/$s
done

# Cursor (프로젝트별 — 각 프로젝트 root 에서)
mkdir -p .cursor/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective cadence-code-principles; do
  ln -s ~/Repository/cadence/$s .cursor/skills/$s
done
```

### Claude Code 메모리 보강 (선택)

Claude Code 는 *별도 메모리 시스템* (`~/.claude/projects/<encoded>/memory/`) 보유. skill 자동 매칭 외에 *메모리 보강* 을 원하면 install.sh 실행:

```bash
cd <your-project>
~/Repository/cadence/cadence-ai-behavior/install.sh        # 7 룰을 프로젝트 메모리에 복제
~/Repository/cadence/cadence-code-principles/install.sh    # 4 코드 원칙 (옵션)
```

`install.sh` 는 cwd 의 메모리 폴더에 룰을 복사하고 `MEMORY.md` 인덱스에 sentinel marker 영역을 갱신/추가. **Codex / Copilot / Cursor 등은 메모리 보강 불필요** — SKILL.md 자체가 본문 + rules/ 디렉토리를 자동 로드.

### Session-start hook (선택, 사용자 명시 승인 시)

도구별 hook 방식 다름:
- **Claude Code**: `~/.claude/settings.json` SessionStart hook (자세한 JSON 은 [using-cadence/SKILL.md § 6](./using-cadence/SKILL.md))
- **OpenAI Codex**: `AGENTS.md` 의 instruction chain — repo root 의 `AGENTS.md` 에 `@~/Repository/cadence/using-cadence/SKILL.md` 같은 형태로 include
- **Cursor**: `.cursorrules` 에 cadence reference 추가
- **Windsurf**: cascade 의 자동 발견 (`~/.agents/skills/` 작동 시 별도 hook 불필요)

## 업데이트

```bash
cd ~/Repository/cadence && git pull
# symlink 가 걸려있으면 git pull 만으로 자동 동기화
# Claude Code 메모리 보강 쓰는 경우 각 프로젝트에서 install.sh --force 재실행
```

## 다른 머신 / 신규 프로젝트 진입 시

1. 본 repo clone (또는 dotfiles 동기화)
2. 위 *도구별 skill 디렉토리 symlink* 1회 실행 (머신당)
3. (Claude Code 사용 시 옵션) 새 프로젝트 디렉토리에서 `install.sh` 1회 실행 — 메모리 보강
4. 각 도구 세션에서 cadence-\* skill 자동 매칭

## 권장 패턴 (프로젝트별 운용)

본 repo 가 *권장* 만 하고 강제 X. 프로젝트 단에서 운용:

- **Post-edit hook (검증 사다리 L1)**: 매 편집 후 결정론 검증 자동 실행 — `tsc`, oxlint/eslint, oxfmt/prettier, build. [cadence-plan § 4. 외부 검증 사다리](./cadence-plan/SKILL.md) 참조
- **회고 / 스펙시트 디렉토리**: 프로젝트 안에 `docs/retrospectives/` + `docs/specsheets/` 운용 권장. cadence-retrospective / cadence-plan 이 cwd 동적 스캔
- **CLAUDE.md / AGENTS.md** 도구별 root config 보유: 도구 매트릭스 (Claude Code, codex, Cursor 등) 호환

## 본 repo 에 *없는* 것

- 개인 코딩 습관 룰 (괄호, switch 지양, 배열 숏폼 등) — linter config 로 강제
- 프로젝트 기술 컨벤션 (React / TanStack / valibot / FSD 등) — 각 프로젝트 안
- 회고 / 스펙시트 자산 — 각 프로젝트 안

`cadence-plan` 의 컨텍스트 수집 단계가 cwd 의 `docs/ai-rules/` + `docs/retrospectives/` + 메모리를 동적 스캔하므로, 프로젝트 종속 룰은 본 repo 없이도 자동으로 참조된다.

## 룰 작성 가이드 (도구 agnostic 보존)

새 룰을 추가할 때 다음 패턴을 따른다 — 특정 도구·모델 이름을 룰에 박지 않기 위한 4가지 원칙.

### 1. 룰 이름은 *현상/원리* 로

❌ `Opus/Sonnet 분리` (도구 명시) <br>
✅ `고추론·고비용 ↔ 저비용·실행 모델 분리` (현상)

❌ `codex 크로스 체크` (도구 명시) <br>
✅ `주 도구 ↔ 보조 도구 크로스 체크` (원리)

### 2. 본문은 *추상 원칙* 으로

도구 이름 대신 *역할* 로 부른다 — "주 도구", "보조 도구", "고추론 모델", "저비용 모델", "AI 도구", "메인 AI" 등.

### 3. 도구별 매핑은 *부속 표/예시* 로 분리

도구별 구체 정보 (Opus 4.x, GPT-5, `codex review --uncommitted` 명령 등) 는 *예시 섹션* 또는 *부록 표* 로 분리. 룰 본문에 박지 않음. 새 도구 추가 시 *표만 갱신* 으로 끝남.

### 4. frontmatter `description` 도 도구 agnostic 으로

Claude Code skill 시스템의 `description` 매칭 정확도를 위해 핵심 어휘는 *도구 일반* 으로. 단 *도구별 예시 포함됨* 정도 명시 가능.

### 5. Historical 인용 / 날짜 / PR 번호는 *제거*

룰 본문에 *특정 사건 / 날짜 / PR 번호 / 사용자 발화 인용* 을 박지 않는다.

❌ `**Why:** 사용자 본인이 2026-04-15 대화에서 직접 명시 — "…"` <br>
✅ `**Why:** AI 의 반사적 동의는 사용자가 못 본 옵션을 묻는다. 결국 되돌리기 비용으로 이어진다.`

❌ `실제 사례 (2026-05-15, PR #186): 메인 레포의 …` <br>
✅ `메인 레포의 다른 작업 브랜치 위에 변경이 쌓이면 patch 추출·복구 절차가 필요해진다.`

이유:
- 룰은 *현재 원칙* 이지 *과거 기록* 이 아님
- 날짜/PR 번호는 *다른 사람이 fork 시 의미 0* — 개인 컨텍스트
- 룰의 *원리* 가 명확하면 *어떤 사건에서 생겼는지* 없어도 적용 가능

*역사 기록* 이 필요하면 회고 (cadence-retrospective) 에서 다룬다 — 룰은 *추출된 원칙* 만.

### 점검 체크리스트

새 룰 commit 전:

- [ ] 룰 이름에 특정 도구/모델 이름 박혀있는가? → *역할/원리* 로 치환
- [ ] 본문에 도구 명시 있는가? → *예시 섹션* 으로 분리
- [ ] frontmatter description 이 도구 일반인가?
- [ ] 도구별 매핑 표가 부속으로 있는가?
- [ ] historical 인용 / 날짜 / PR 번호가 박혀있는가? → 제거하고 *원리* 만
