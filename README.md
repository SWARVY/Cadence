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
  <strong>실행은 이어가고, 결정은 함께하세요.</strong>
  <br/>
  <sub>AI가 승인된 범위에서 일하고, 결과가 달라지는 결정점에서 개발자에게 돌아오는 협업 리듬.</sub>
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

> *좋은 AI 협업은 자주 멈추는 것이 아니라, 필요한 곳에서 정확히 멈추는 것입니다.*

cadence는 AI 코딩 에이전트를 위한 **decision-gated collaboration workflow**입니다. 승인된 범위의 가역적 탐색, 편집, 검증은 이어서 수행하고, 사용자 선택·범위·공개 계약·비가역 작업·승인되지 않은 외부 상태가 달라지는 지점에서 보고 후 정지합니다.

정확도 체크는 유지합니다. 불필요한 진행 승인만 줄입니다.

---

## 빠른 시작

**설치**

```bash
npx skills add https://github.com/SWARVY/Cadence --all
```

**권장 bootstrap**

프로젝트 `AGENTS.md` 또는 도구별 root config에 최소 진입점을 둡니다. 이 repo의 [AGENTS.md](./AGENTS.md)를 그대로 사용할 수 있습니다.

```markdown
항상 cadence의 decision-gated 리듬을 따른다.
승인된 범위 안의 가역적 탐색·편집·검증과 명시적으로 승인된 외부 단계는 이어서 수행한다.
사용자 선택, 범위, 공개 계약, 비가역 작업, 승인되지 않은 외부 상태가 달라지는 결정점에서 보고 후 정지한다.
리뷰·계획 요청을 구현 승인으로 확대하지 않으며, 하위 skill의 phase 전환만으로 사용자 게이트를 추가하지 않는다.
리뷰의 질문·제안·의견과 완곡한 질문형 제안은 별도 실행 요청이 없으면 견해를 먼저 답하고, 직전의 구체적 추천 승인과 구분한다.
리뷰 수용 전에는 현재 구현 이유·제약과 결론을 뒤집을 실제 적용 전제를 확인하고, 제안 평가·추천과 근거를 편집 전에 짧게 공유한다.
사용자 선택 전에는 선택지가 실제로 관찰·비교 가능한지 확인한다.
plan task 수를 reviewer 호출 수로 사용하지 않고, 같은 위험·불변식·증거를 공유하는 변경은 review slice로 묶는다.
하위 skill의 절차나 검증 성공은 commit 권한을 만들지 않으며, 완료된 변경 사이클의 권한을 새 변경에 승계하지 않고 실제 성공한 상태 변경만 완료로 보고한다.
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

특정 도구가 공식 skill 디렉토리를 요구하면 그 위치에 같은 방식으로 symlink합니다.

</details>

<details>
<summary><strong>프로젝트 메모리 보강</strong></summary>

일부 도구는 `SKILL.md` 외에 별도 메모리 시스템을 사용합니다.

```bash
cd <your-project>
~/Repository/Cadence/skills/cadence-ai-behavior/install.sh
```

기본 target은 `~/.agents/projects/<encoded-cwd>/memory`입니다. 다른 위치가 필요하면 `CADENCE_MEMORY_DIR=/path/to/memory`로 지정합니다.

</details>

---

## 왜 cadence인가

AI에게 *"이 기능 만들어줘"*라고 하면 탐색부터 커밋까지 하나의 흐름으로 이어지기 쉽습니다. 반대로 모든 내부 phase에서 승인을 요구하면 사용자는 `진행하자` 버튼만 반복해서 누르게 됩니다.

cadence는 두 극단 사이를 선택합니다.

| full-ai-driven | step-gated 과잉 | cadence |
|:---|:---|:---|
| AI가 범위와 외부 작업까지 자동 진행 | 내부 phase마다 정지 | 승인 범위 안의 가역적 작업은 지속 |
| 사용자는 마지막 결과만 검수 | 사용자는 진행 승인을 반복 | 결과가 달라지는 결정만 함께 선택 |
| 첫 안이 그대로 구현 | 실질적 대안이 없어도 옵션을 생성 | 유효한 대안이 있을 때만 비교 |
| commit / push가 자연스럽게 이어짐 | 승인된 외부 단계도 다시 질문 | terminal intent까지만 수행 |

반복 실패는 대개 코드 생성 능력보다 경계 판단에서 생깁니다.

- **놓친 옵션**: 여러 유효한 해석이 있는데 첫 안으로 고정
- **stale 가정**: 기존 시스템과 contract를 보기 전에 구현
- **범위 확대**: 리뷰나 계획 요청을 코드 편집으로 확장
- **반사적 동의**: 사용자 의견을 검토하지 않고 그대로 수용
- **적용 전제 누락**: 일반론은 맞지만 현재 호출·렌더링 경로에는 적용되지 않음
- **원격 과잉 실행**: 로컬 작업 뒤 commit / push / PR까지 진행
- **증거 없는 완료 보고**: 실행하지 않은 Git·외부 상태를 완료로 표시
- **준비되지 않은 선택지**: 보이지 않거나 구분되지 않는 산출물로 결정 요구
- **empty approval loop**: 새 선택 없이 `진행하자`만 반복 요구
- **review fan-out**: 계획 task마다 독립 reviewer를 붙여 같은 불변식을 반복 검토

cadence는 더 많은 정지를 만들지 않습니다. **정확도 체크와 사용자 게이트를 분리합니다.**

---

## 핵심 개념

### Decision Gate

다음 행동이 사용자 선택에 따라 달라질 때만 보고 후 정지합니다.

- 승인된 범위 또는 Out of scope 변경
- 승인에 없던 공개 API / schema / 데이터 계약 / 아키텍처 변경
- 비가역적·파괴적 작업
- 승인되지 않은 commit / push / PR / merge / 댓글 / 배포
- 안전한 기본값이 없는 모호성
- 접근의 전제를 깨는 검증 실패

판단 질문은 하나입니다.

> 지금 사용자에게 돌려보냈을 때 새로 선택할 것이 있는가?

선택이 필요하다면 먼저 비교 산출물이 실제로 열리거나 렌더링되고, 차이가 관찰 가능하며, 핵심 제약과 검증 결과가 준비됐는지 확인합니다.

### Approval Scope

| 요청 | 승인 범위 |
|:---|:---|
| 확인 / 분석 / 리뷰 | 읽기와 보고 |
| 계획 | 탐색, 옵션, 위험, 계획 문서화 |
| 구현 / 수정 | 합의된 범위의 로컬 편집과 검증 |
| 커밋 | commit까지. push 없음 |
| PR 올려줘 | 최신 검증, 필요한 branch / commit, push, PR 생성. merge 없음 |
| 머지해줘 | PR merge까지. main sync / 설치본 갱신 없음 |

`진행하자`, `좋아` 같은 짧은 승인은 직전에 명시된 제안과 원래 요청 경계까지만 승계합니다.

### Gate와 checkpoint

- **Gate**: 새 사용자 결정을 기다리며 정지
- **Checkpoint**: 승인된 흐름의 단계 결과를 보고하고 계속 진행

예를 들어 `PR 올려줘` 뒤 commit 완료 보고는 checkpoint입니다. push와 PR 생성이 이미 승인됐다면 같은 허가를 다시 묻지 않습니다.

---

## 리듬

```text
요청
  ↓
산출물 + 결정 위험 + 실행 범위 + 승인 범위 분류
  ↓
Context / Options / Risk / Verification 내부 체크
  ↓
선택지가 실제로 관찰·비교 가능한가?
  ↓
새 사용자 선택이 필요한가?
  ├─ 아니오 → 승인 범위 안의 편집·검증·외부 단계 지속
  └─ 예     → 차이·영향·추천 보고 후 정지
  ↓
결과와 검증 보고
  ↓
Retrospective → recurring pattern → behavior rule
```

실행량과 결정 위험은 분리합니다.

| 결정 위험 | 실행 범위 | 기본 진행 |
|:---|:---|:---|
| 낮음 | 작음 | 바로 수행 후 결과 보고 |
| 낮음 | 큼 | dry-run, 내부 표본 검토, 일괄 수행 |
| 높음 | 작음 | 핵심 결정 1회 합의 후 수행 |
| 높음 | 큼 | 의미 있는 결정점별 진행 |

파일 수가 많다는 이유만으로 사용자 게이트가 늘어나지 않습니다.

계획 task, review slice, commit unit도 분리합니다. 같은 위험과 검증 증거를 공유하는 task는 함께 검토하고, 문구·경로·format·기계적 이동은 결정론적 검사와 표본 diff로 닫습니다. 하위 workflow가 task별 review를 권장하더라도 사용자가 명시하지 않았다면 실행 시점의 위험 기반 topology가 우선합니다.

---

## Skills

cadence는 4개의 skill로 나뉩니다.

| skill | 역할 | 발동 시점 |
|:---|:---|:---|
| [using-cadence](./skills/using-cadence/SKILL.md) | 승인 범위, decision-gating, 라우팅, 사용자 게이트 소유 | coding, debugging, review, planning 시작 |
| [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) | 반사적 동의, 산출물 혼동, 자동 원격 반영, 외부 도구 재시도 통제 | 모든 AI 응답 turn |
| [cadence-plan](./skills/cadence-plan/SKILL.md) | 기존 시스템 적합성, 옵션, 선택지 준비도, 위험 / 폐기 / Out of scope, 위험 기반 review topology와 비용 비례 검증 | 높은 결정 위험, 큰 실행 범위, 신규 spec, 모호 작업 |
| [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) | 작업 완료 후 회고, 로컬 문서 묶음, 트랜스크립트 마이닝, 룰 승급 | 완료, 실패, mid-PR 학습, 룰 위반 |

하위 skill은 판단 렌즈를 제공합니다. 사용자에게 보이는 게이트의 최종 소유자는 `using-cadence`입니다.

---

## 작동 신호

| 신호 | 의미 |
|:---|:---|
| "요청은 A인데 기존 패턴은 B" | 기존 시스템과 요청 충돌 |
| "옵션 A / B + 내 추천" | 결과를 바꾸는 실질적 선택 |
| "실질적 대안 없음" | 억지 옵션 생성 없이 기계적 경로 선택 |
| "이 요청은 문서 패치로 이해" | 산출물 분류 |
| "commit `<hash>` 완료, push 진행" | 실제 결과가 확인된 승인 외부 흐름의 checkpoint |
| "여기부터 승인 범위 밖" | decision gate |
| "같은 인증 / 세션 오류 2회" | stale session 반복 중단 |
| "회고 가치 평가" | 현재 retrospective 규칙 발동 |

내부 phase 이름이나 작업 크기 분류가 매번 출력되면 정상 동작이 아닙니다.

---

## 룰 layer

| Layer | 정체 | 위치 |
|:---|:---|:---|
| **A. AI 행동 통제** | 반사적 동의, 산출물 분류, 원격 작업, 도구 실패 | [cadence-ai-behavior](./skills/cadence-ai-behavior/SKILL.md) |
| **A'. AI 작업 프로세스** | decision-gating, 계획 체크, 검증, 회고 | [using-cadence](./skills/using-cadence/SKILL.md), [cadence-plan](./skills/cadence-plan/SKILL.md), [cadence-retrospective](./skills/cadence-retrospective/SKILL.md) |
| **B. 개인 코딩 습관** | 괄호, 배열 숏폼, type vs interface | linter / formatter |
| **C. 코딩 판단 원칙** | 단언, disable, co-location, 추상화 판단 | stack 특화 skill repo |
| **L2. 프로젝트 기술 컨벤션** | 프레임워크, 디자인 토큰, validation | 프로젝트 root config / `docs/ai-rules/` |
| **L3. 프로젝트 도메인 결정** | 특정 화면 / 도메인 결정 | 프로젝트 메모리 / specsheets |

본 repo는 **A + A'**를 다룹니다.

---

## Fork guide

새 룰을 추가할 때는 네 가지를 지킵니다.

1. 룰 이름은 도구명이 아니라 반복 실패 현상으로 작성
2. 본문은 도구·도메인과 분리된 원칙으로 작성
3. 도구별 매핑은 부록이나 프로젝트 설정에 배치
4. 날짜, PR 번호, 과거 사건은 retrospective에 기록

공용 저장소의 retrospective는 프로젝트·고객 이름, 내부 endpoint, commit·PR 식별자, 개인 발화 직접 인용을 제거하고 반복 실패 메커니즘과 수용 기준으로 일반화합니다. 원본 증거는 source 프로젝트의 비공개 회고에 둡니다.

---

## 더 읽기

- [USAGE.md](./USAGE.md): 설치, 회귀 시나리오, 진단표
- [using-cadence](./skills/using-cadence/SKILL.md): 승인 범위와 decision-gating
- [cadence-plan](./skills/cadence-plan/SKILL.md): 4개 정확도 체크와 검증 사다리
- [cadence-retrospective](./skills/cadence-retrospective/SKILL.md): 회고와 룰 승급
- [회고 인덱스](./notes/INDEX.md): cadence 자체의 반복 실패와 룰 진화 기록

---

<p align="center">
  <em>AI는 혼자 결정하지 않습니다.</em>
  <br/><br/>
  <strong>좋은 협업에는 리듬이 있습니다.</strong>
</p>
