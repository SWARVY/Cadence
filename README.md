<div align="center">

# cadence

**전체 자동화를 멈추세요. 페이스를 시작하세요.**

AI 가 *한 스텝 산출물* 만 만들고, 개발자가 *다음 스텝* 을 결정한다.
자전거의 cadence, 음악의 cadence — *함께 만드는 리듬* 이 핵심.

</div>

<p align="center">
  <code>npx skills add https://github.com/SWARVY/Cadence --all</code>
</p>

<p align="center">
  <a href="#철학-full-ai-driven-의-함정">철학</a> ·
  <a href="#step-gating-사이클">step-gating</a> ·
  <a href="#skills">Skills</a> ·
  <a href="#빠른-시작">빠른 시작</a> ·
  <a href="./USAGE.md">사용 가이드</a>
</p>

---

## 철학: full-ai-driven 의 함정

AI 에게 *"이 기능 만들어줘"* 한 줄을 던지면 — 플랜 / 코딩 / 테스트 / 커밋까지 자동으로 흘러간다. 빠르지만 위험하다.

- **놓친 옵션** — AI 가 *첫 안* 으로 진행. 더 나은 옵션은 영영 묻힘
- **stale 가정** — 회고 / 기존 컴포넌트를 확인 안 한 채 *추상화 결정*
- **mid-PR 회수** — 머지 직전 *외부 변경* 발견 → 되돌리기 비용 폭증
- **사용자 의견 묻힘** — AI 의 *반사적 동의* (sycophancy) 가 더 나은 안을 차단

cadence 는 *반대 방향* 으로 간다.

<div align="center">

| full-ai-driven | cadence (step-gating) |
| :--- | :--- |
| AI 가 N 단계 자동 진행 | AI 는 *한 스텝 산출물만*, 보고 후 정지 |
| 사용자 = *결과 검수자* | 사용자 = *동료* — 매 스텝 결정 |
| 옵션 1 안 + 자동 실행 | 옵션 2 안 + Contrarian → 선택 → 진행 |
| commit / push 자동 | 명시 요청 시만 — 워크플로우 끝에서 정지 |

</div>

> *"AI 가 한 스텝 산출물만 만들고 보고 후 정지. 개발자 피드백 후 다음 스텝."*

## step-gating 사이클

```
작은 작업 (≤ 10분)        → 1 step, 결과 보고만
중간 작업                 → 2-3 step 압축
큰 작업                   → 4 step 사이클:

  Step 1.  컨텍스트 수집           📝 보고  →  👤 검토
  Step 2.  옵션 + Contrarian      📝 보고  →  👤 선택
  Step 3.  위험 / 폐기 / OoS      📝 보고  →  👤 승인
  Step 4.  검증 사다리             📝 보고  →  👤 결정
                                              ↓
                              작업 완료
                                  ↓
                      cadence-retrospective (회고)
                                  ↓
              (recurring 패턴)  룰화 승급
                                  ↓
                    cadence-ai-behavior 갱신
                                  ↓
                       다음 작업의 컨텍스트
```

작은 작업은 1 step (게이트 0-1). 중간 2-3 step. 큰 작업만 4 step mandatory. **자동 chain 없음** — 매 게이트가 *개발자의 결정 지점*.

## Skills

| skill | 담당 | 적용 시점 |
| :--- | :--- | :--- |
| [using-cadence](./skills/using-cadence/SKILL.md) | **메타 오케스트레이터** — 라우팅 / 우선순위 / step-gating | 매 turn 첫 점검 |
| [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) | AI 행동 통제 룰 — sycophancy / 즉시 편집 / 자동 push 통제 | 모든 AI 응답 turn |
| [cadence-plan](./skills/cadence-plan/SKILL.md) | 큰 작업 4단 + 스펙시트 helper lens + 메타-구조 + 검증 사다리 | 큰 작업, 신규 spec, 모호 작업, 추상화 결정 |
| [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) | 회고 + 트랜스크립트 마이닝 + 룰화 승급 | 작업 완료 / 실패 / mid-PR 학습 / 룰 위반 발견 |

cadence 는 **cross-stack 범용 협업 워크플로우** 만 담는다. *언어 / 프레임워크 / stack 특화 룰* 은 별도 repo 로 분리하여 fork 자가 자기 stack 만 install.

```
cadence-plan (진입)  →  실행  →  cadence-retrospective (학습)
       ↑                                       │
       └─── 룰화 승급 → cadence-ai-behavior ←──┘
```

## 빠른 시작

<p align="center">
  <code>npx skills add https://github.com/SWARVY/Cadence --all</code>
</p>

skills CLI 가 `skills/` 아래의 4개 skill 을 탐색해 설치한다. 특정 skill 만 설치하거나 수동 symlink 를 쓰는 절차는 [USAGE.md](./USAGE.md) 참조.

### Root bootstrap (권장)

`using-cadence` / `cadence-ai-behavior` 처럼 거의 매 turn 적용되어야 하는 규칙은 skill description 매칭만 믿지 말고, 프로젝트의 `AGENTS.md` 또는 도구별 root config 에 짧은 bootstrap 을 함께 둔다.

```markdown
항상 cadence 의 기본 리듬을 따른다: 작업 크기를 먼저 판정하고, 한 스텝 산출물만 만든 뒤 보고 후 정지한다. 사용자 피드백을 받은 다음 단계로 진행하며, 자세한 절차는 설치된 `using-cadence` / `cadence-ai-behavior` skill 을 로드한다.
```

상세 절차는 skill 에 남기고 root config 에는 이 짧은 진입점만 두는 편이 context 비용과 발동 안정성의 균형이 좋다.

### 도구별 메모리 보강 (선택)

skill 자동 매칭 외 *결정론적 메모리 적용* 이 필요한 도구라면 해당 도구의 메모리/root config 에 cadence 룰을 보강한다. 이 repo 의 `install.sh` 는 별도 프로젝트 메모리를 운용하는 환경을 위한 helper 다.

```bash
cd <your-project>
~/Repository/Cadence/skills/cadence-ai-behavior/install.sh
```

기본 target 은 `~/.agents/projects/<encoded-cwd>/memory` 이며, 도구가 다른 메모리 경로를 요구하면 `CADENCE_MEMORY_DIR=/path/to/memory` 로 지정한다.

SKILL.md 자체를 직접 읽는 도구라면 별도 메모리 보강 없이도 동작할 수 있다.

## 작업 크기별 cadence

| 작업 크기 | step 수 | 게이트 | 산출물 |
| :--- | :---: | :---: | :--- |
| 작은 (≤ 10분) | 1 step | 0-1 | 결과 보고만 |
| 중간 (10–30분) | 2-3 step | 1-2 | 얇은 스펙시트 |
| 큰 (≥ 30분 / 새 도메인 / 추상화) | 4 step | 3-4 mandatory | 스펙시트 메타-구조 |

## 룰 layer 분리

cadence 의 핵심 설계 — 룰을 정체에 따라 *다른 위치* 에 둔다.

| 분류 | 정체 | 위치 |
| :--- | :--- | :--- |
| **A. AI 행동 통제** | sycophancy / 즉시 편집 / 자동 push — *AI 특유 경향* 통제 | 본 repo [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) |
| **A'. AI 작업 프로세스** | 큰 작업 plan 4단 + 스펙시트 helper lens + 검증 사다리 + 회고 | 본 repo [cadence-plan](./skills/cadence-plan/SKILL.md) + [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) |
| **B. 개인 코딩 습관** | 괄호 / 배열 숏폼 / type vs interface — *취향*, linter 강제 가능 | 각 프로젝트의 linter config |
| **C. 개인 코딩 판단 원칙** | 단언 / disable / 인라인 / co-location — *언어 / 프레임워크별 예시 다름* | 별도 stack 특화 skill repo |
| **L2. 프로젝트 기술 컨벤션** | 프레임워크 버전 / 검증 라이브러리 / 디자인 토큰 — *프로젝트 종속* | 각 프로젝트의 `docs/ai-rules/` · root config · 메모리 |
| **L3. 프로젝트 도메인 결정** | 특정 화면 / 도메인 결정 | 각 프로젝트 메모리 |

본 repo 는 **A + A' (cross-stack 범용)** 만. B / C / L2 / L3 는 본 repo 밖.

## 룰 작성 가이드 (fork 자용)

새 룰 추가 시 4가지 원칙:

#### 1. 룰 이름은 *현상 / 원리* 로

도구 / 모델 이름을 룰 이름에 박지 않는다.

#### 2. 본문은 *추상 원칙* 으로

도구 이름 대신 *역할* 로 — "주 도구", "보조 도구", "고추론 모델", "AI 도구"

#### 3. 도구별 매핑은 *부속 표 / 예시* 로 분리

구체 정보는 *부록 표* 에 두고 룰 본문에 박지 않는다. 새 도구 추가 시 *표만 갱신* 으로 끝남.

#### 4. Historical 인용 / 날짜 / PR 번호는 *제거*

룰은 *현재 원칙* 이지 *과거 기록* 이 아니다. 역사 기록이 필요하면 cadence-retrospective 에서 다룬다.

## FAQ

**Q. cadence 가 너무 무거워요. 작은 작업까지 게이트?** <br>
A. 의도된 동작 아님 — 작업 크기 판정이 작동하면 작은 작업은 1 step. [USAGE.md § 진단표](./USAGE.md) 참조.

**Q. AskUserQuestion 으로 매번 물어보는데 부담돼요.** <br>
A. *AskUserQuestion 강요 함정* — cadence 가 제대로 작동하면 *자유 응답* 받아야 정상.

**Q. 일부 skill 만 쓸 수 있나요?** <br>
A. 각 skill 독립 발동. symlink 안 걸면 그 skill 만 skip.

**Q. fork 해서 자기 선호로 바꿔도 되나요?** <br>
A. 권장. 룰 작성 가이드 따르면 일관성 유지.

## 권장 패턴

본 repo 가 *권장* 만 하고 강제 X:

- **Post-edit hook** (검증 사다리 L1): 매 편집 후 결정론 검증 — `tsc`, linter, formatter, build
- **회고 / 스펙시트 디렉토리**: 프로젝트 안 `docs/retrospectives/` + `docs/specsheets/` — cadence-plan / retrospective 가 cwd 동적 스캔
- **스펙시트 helper lens**: 요구가 모호하면 brainstorming 계열, 결정된 내용을 문서화할 때 writing-skills / clarify 계열을 lazy-load. 없으면 cadence-plan 의 체크리스트로 대체
- **도구별 root config**: `AGENTS.md` 등 프로젝트 지시 파일

## 관련

- [USAGE.md](./USAGE.md) — 시나리오 5종 + 발동 시그널 + 진단표 + 점진적 도입
