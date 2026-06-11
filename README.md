<p align="center">
  <br/>
  ◯ ─────────── ◯
  <br/><br/>
  <strong>C A D E N C E</strong>
  <br/><br/>
  ◯ ─────────── ◯
  <br/>
</p>

<p align="center">
  <strong>전체 자동화를 멈추세요. 페이스를 시작하세요.</strong>
  <br/>
  <sub>AI 가 한 스텝 산출물만 만들고, 개발자가 다음 스텝을 결정하는 협업 리듬.</sub>
</p>

<p align="center">
  <code>npx skills add https://github.com/SWARVY/Cadence --all</code>
</p>

<p align="center">
  <a href="#빠른-시작">빠른 시작</a> ·
  <a href="#왜-cadence인가">철학</a> ·
  <a href="#리듬">리듬</a> ·
  <a href="#skills">Skills</a> ·
  <a href="#룰-layer">Layer</a> ·
  <a href="./USAGE.md">사용 가이드</a>
</p>

> *AI 는 오래 달릴수록 똑똑해지는 게 아니라, 멈춰야 할 지점을 자주 놓칩니다.*

cadence 는 AI 코딩 에이전트를 위한 **step-gated collaboration workflow** 입니다. AI 가 플랜, 구현, 검증, 커밋, 푸시까지 한 번에 이어 달리는 대신, 한 스텝의 산출물을 만들고 보고한 뒤 멈춥니다.

핵심은 속도를 늦추는 것이 아닙니다. **되돌릴 수 있는 지점에서 같이 결정하는 것** 입니다.

---

## 빠른 시작

**설치** — skills CLI 가 `skills/` 아래의 4개 skill 을 탐색합니다.

```bash
npx skills add https://github.com/SWARVY/Cadence --all
```

**권장 bootstrap** — 거의 모든 turn 에 적용되어야 하는 최소 리듬은 프로젝트 `AGENTS.md` 또는 도구별 root config 에 짧게 둡니다.

```markdown
항상 cadence 의 기본 리듬을 따른다: 작업 크기를 먼저 판정하고, 한 스텝 산출물만 만든 뒤 보고 후 정지한다. 사용자 피드백을 받은 다음 단계로 진행하며, 자세한 절차는 설치된 `using-cadence` / `cadence-ai-behavior` / `cadence-retrospective` skill 을 로드한다. PR merge/머지 직후에는 다음 작업 전에 `회고 가치 평가: 낮음 / 중간 / 높음` 을 먼저 출력한다.
```

<details>
<summary><strong>수동 symlink</strong></summary>

```bash
git clone https://github.com/SWARVY/Cadence.git ~/Repository/Cadence

mkdir -p ~/.agents/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective; do
  ln -s ~/Repository/Cadence/skills/$s ~/.agents/skills/$s
done
```

특정 도구가 공식 skill 디렉토리를 따로 요구하면 그 위치에 같은 방식으로 symlink 합니다.

</details>

<details>
<summary><strong>프로젝트 메모리 보강</strong></summary>

일부 도구는 `SKILL.md` 외에 프로젝트 메모리 시스템을 별도로 운용합니다. 그런 환경에서는 선택적으로 AI 행동 룰을 현재 프로젝트 메모리에 복제합니다.

```bash
cd <your-project>
~/Repository/Cadence/skills/cadence-ai-behavior/install.sh
```

기본 target 은 `~/.agents/projects/<encoded-cwd>/memory` 입니다. 다른 경로가 필요하면 `CADENCE_MEMORY_DIR=/path/to/memory` 로 지정합니다.

</details>

---

## 왜 cadence인가

AI 에게 *"이 기능 만들어줘"* 한 줄을 던지면, 플랜에서 커밋까지 자연스럽게 이어집니다. 빠르지만 자주 비쌉니다.

| full-ai-driven | cadence |
|:---|:---|
| AI 가 여러 단계를 자동 진행 | AI 는 한 스텝 산출물만 만들고 정지 |
| 사용자는 결과 검수자 | 사용자는 매 스텝의 동료 결정자 |
| 첫 번째 안이 그대로 구현 | 최소 2안 + Contrarian 으로 선택지 확보 |
| 커밋 / 푸시까지 흐름이 이어짐 | 명시 요청 전에는 로컬 결과 보고에서 정지 |

반복해서 터지는 실패는 대부분 코드 생성 능력 문제가 아닙니다.

- **놓친 옵션** — 첫 안이 그럴듯해서 더 나은 안이 묻힘
- **stale 가정** — 회고 / 기존 시스템 / 프로젝트 룰을 보기 전에 추상화 결정
- **mid-PR 회수** — 머지 직전 contract gap 을 발견해 되돌리기 비용 증가
- **반사적 동의** — 사용자의 의견을 검토하지 않고 그대로 수용
- **응답 대상 혼동** — 짧은 "수정 / 반영" 지시를 텍스트 답변인지 코드 편집인지 분류하지 못함
- **stale 세션 재시도** — 외부 도구 인증 / 세션 실패를 같은 방식으로 반복 호출

cadence 는 이 실패를 *더 많은 자동화* 로 해결하지 않습니다. **작은 결정 지점** 을 더 자주 만듭니다.

---

## 리듬

```text
작은 작업       →  실행 후 결과 보고
중간 작업       →  컨텍스트 + 옵션  →  실행 / 검증
큰 작업         →  4 step cycle

Step 1  Context       →  보고  →  사용자 검토
Step 2  Options       →  보고  →  사용자 선택
Step 3  Risk / OoS    →  보고  →  사용자 승인
Step 4  Verification  →  보고  →  사용자 결정

완료
  ↓
Retrospective
  ↓
Recurring pattern
  ↓
Behavior rule
  ↓
다음 작업의 컨텍스트
```

작은 작업까지 거창하게 만들지 않습니다. 큰 작업을 한 번에 밀지도 않습니다.

| 작업 크기 | cadence | 산출물 |
|:---|:---|:---|
| 작은 (≤ 10분) | 1 step | 결과 보고 |
| 중간 (10-30분) | 2-3 step | 얇은 스펙시트 또는 플랜 요약 |
| 큰 (≥ 30분 / 새 도메인 / 추상화) | 4 step | 스펙시트 + 검증 사다리 |

---

## Skills

cadence 는 4개의 skill 로 나뉩니다. 하나의 거대한 규칙 파일이 아니라, 필요한 순간에 필요한 렌즈만 로드합니다.

| skill | 역할 | 발동 시점 |
|:---|:---|:---|
| [using-cadence](./skills/using-cadence/SKILL.md) | 라우팅 / 우선순위 / step-gating | coding, debugging, review, planning turn 의 첫 점검 |
| [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) | sycophancy, 응답 산출물 분류, 즉시 편집, 자동 push, 외부 도구 재시도, 경로 혼동 같은 AI 행동 통제 | 모든 AI 응답 turn |
| [cadence-plan](./skills/cadence-plan/SKILL.md) | 기존 시스템 적합성, 큰 작업 4단, 옵션 탐색, 위험 / 폐기 / Out of scope, 검증 사다리 | 큰 작업, 신규 spec, 모호 작업, 추상화 결정 |
| [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) | 작업 완료 후 회고, 트랜스크립트 마이닝 후보 분류, 룰화 승급 | 완료, 실패, mid-PR 학습, 룰 위반 발견 |

```text
cadence-plan  →  실행  →  cadence-retrospective
      ↑                         │
      └──── behavior rule ◄─────┘
```

---

## 작동 신호

정상적으로 적용되면 AI 응답에서 이런 신호가 보입니다.

| 신호 | 의미 |
|:---|:---|
| "이건 작은/중간/큰 작업으로 보입니다" | 작업 크기 판정 |
| "옵션 A / B / C" + "내 추천" | 단일 안 잠김 방지 |
| "Contrarian" | 반대 가정 검토 |
| "기존 시스템은 B인데 요청은 A" | 기존 UI / API / copy / workflow 와 사용자 요청의 차이를 먼저 드러냄 |
| "위험 / 폐기 조건 / Out of scope" | 머지 직전 회수 비용 줄이기 |
| "즉시 편집 대신 견해 교환부터" | 리뷰를 수정 지시가 아닌 대화로 처리 |
| "이 지시는 문서 패치로 이해하고 진행" | 짧은 지시에서 산출물이 텍스트 / 문서 / 코드 / 원격 작업 중 무엇인지 분류 |
| "같은 인증 / 세션 오류 2회" | 외부 도구 stale session 반복 호출을 멈추고 이어받기 요약으로 전환 |
| "회고 가치 평가: 낮음 / 중간 / 높음" + "회고 처리: 작성 / 보류 / 생략 / 미결" | PR merge 직후 학습 신호를 놓치지 않고, 중간/높음 회고를 다음 작업 전에 닫기 |

더 자세한 실제 대화 예시는 [USAGE.md](./USAGE.md)를 참고하세요.

---

## 룰 layer

cadence 는 모든 취향을 여기에 넣지 않습니다. 규칙의 정체에 따라 위치를 나눕니다.

| Layer | 정체 | 위치 |
|:---|:---|:---|
| **A. AI 행동 통제** | 반사적 동의, 응답 산출물 분류, 즉시 편집, 자동 push, 외부 도구 실패 반복 중단, 장황한 주석 | [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) |
| **A'. AI 작업 프로세스** | step-gating, 스펙시트, 검증 사다리, 회고 | [cadence-plan](./skills/cadence-plan/SKILL.md), [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) |
| **B. 개인 코딩 습관** | 괄호, 배열 숏폼, type vs interface 같은 취향 | linter / formatter |
| **C. 코딩 판단 원칙** | 단언, disable, co-location, 추상화 판단 | stack 특화 skill repo |
| **L2. 프로젝트 기술 컨벤션** | 프레임워크, 검증 라이브러리, 디자인 토큰 | 프로젝트 `docs/ai-rules/`, root config, 메모리 |
| **L3. 프로젝트 도메인 결정** | 특정 화면 / 도메인 결정 | 프로젝트 메모리 / specsheets |

본 repo 는 **A + A'** 만 다룹니다. fork 해서 자기 stack 의 C layer 를 붙이는 것을 권장합니다.

---

## Fork guide

새 룰을 추가할 때는 네 가지를 지킵니다.

1. **룰 이름은 현상 / 원리로**  
   도구나 모델 이름을 박지 않습니다.

2. **본문은 추상 원칙으로**  
   "Codex" 대신 "주 도구", "보조 도구", "AI 도구" 같은 역할 이름을 씁니다.

3. **도구별 매핑은 부록으로**  
   새 도구가 생기면 표만 바꾸면 되게 둡니다.

4. **역사는 회고로**  
   날짜, PR 번호, 과거 사건은 룰 본문이 아니라 retrospective 에 남깁니다.

---

## 더 읽기

- [USAGE.md](./USAGE.md) — 설치, 시나리오, 진단표, 점진적 도입
- [using-cadence](./skills/using-cadence/SKILL.md) — 메타 라우팅과 step-gating
- [cadence-plan](./skills/cadence-plan/SKILL.md) — 큰 작업 플랜과 검증 사다리
- [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) — 회고와 룰화 승급

---

<p align="center">
  <em>AI 는 혼자 달리지 않습니다.</em>
  <br/><br/>
  <strong>좋은 협업에는 리듬이 있습니다.</strong>
</p>
