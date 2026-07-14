# cadence 운영 가이드

README가 철학과 구조를 설명한다면, 이 문서는 실제 세션에서 기대할 행동과 회귀 시나리오를 정의한다.

- 처음 설치하고 작동을 확인하는 법
- 결정 위험과 실행 범위에 따른 진행 방식
- Approval Scope와 외부 작업 경계
- cadence가 발동하지 않을 때 점검할 것

## 1. 처음 설치

### 1-1. Skill 설치

```bash
npx skills add https://github.com/SWARVY/Cadence --all
```

repo의 `skills/` 아래 4개 skill을 설치한다. 일부만 설치하려면 `--skill using-cadence`처럼 선택한다.

### 1-2. Root bootstrap

프로젝트 `AGENTS.md` 또는 도구별 root config에 최소 진입점을 둔다. 상세 절차는 skill이 담당한다.

```markdown
항상 cadence의 decision-gated 리듬을 따른다.
승인된 범위 안의 가역적 탐색·편집·검증과 명시적으로 승인된 외부 단계는 이어서 수행한다.
사용자 선택, 범위, 공개 계약, 비가역 작업, 승인되지 않은 외부 상태가 달라지는 결정점에서 보고 후 정지한다.
리뷰·계획 요청을 구현 승인으로 확대하지 않으며, 하위 skill의 phase 전환만으로 사용자 게이트를 추가하지 않는다.
```

### 1-3. 수동 symlink

```bash
git clone https://github.com/SWARVY/Cadence.git ~/Repository/Cadence

mkdir -p ~/.agents/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective; do
  ln -s ~/Repository/Cadence/skills/$s ~/.agents/skills/$s
done
```

특정 도구가 공식 skill 디렉토리를 요구하면 그 위치를 우선한다.

## 2. 핵심 운용

### 2-1. 내부 분류

AI는 매 요청에서 다음을 내부적으로 분류한다.

1. 산출물: text / document patch / code edit / local git / remote action
2. 결정 위험: 낮음 / 높음
3. 실행 범위: 작음 / 큼
4. 승인 범위: 이번 요청이 허용한 행동과 종료 지점

분류 자체가 사용자 선택을 만들지 않으면 출력하지 않는다.

### 2-2. Decision Gate

다음 행동이 사용자 선택에 따라 달라질 때만 보고 후 정지한다.

- 승인 범위 또는 Out of scope 변경
- 승인에 없던 공개 API / schema / 데이터 계약 / 아키텍처 변경
- 파괴적이거나 비가역적인 작업
- 승인되지 않은 commit / push / PR / merge / 댓글 / 배포
- 안전한 기본값이 없는 모호성
- 현재 접근의 전제를 깨는 검증 실패
- 사용자 소유 변경과 해결할 수 없는 충돌

내부 phase나 helper skill 전환은 게이트 사유가 아니다.

### 2-3. Approval Scope

| 요청 | 승인 범위 |
| --- | --- |
| 확인 / 분석 / 리뷰 | 읽기와 보고 |
| 계획 | 탐색, 옵션, 위험, 계획 문서화 |
| 구현 / 수정 | 합의된 범위의 로컬 편집과 검증 |
| 커밋 | commit까지. push 없음 |
| 푸시 | 이미 commit된 현재 변경의 push |
| PR 올려줘 | 최신 검증, 필요한 branch / commit, push, PR 생성. merge 없음 |
| 머지해줘 | PR merge. main sync / branch 삭제 / 설치본 갱신 없음 |

원래 요청이 구현이고 사용자가 검토된 추천안에 `진행하자`, `그렇게 가자`, `좋아`라고 답하면 상세 계획, 로컬 편집, 테스트를 이어간다.

짧은 승인은 직전에 명시된 제안과 원래 요청 경계까지만 적용한다. 리뷰나 계획 요청을 구현 승인으로 확대하지 않는다.

### 2-4. Gate와 checkpoint

- **Gate**: 새 사용자 결정을 기다리며 응답 종료
- **Checkpoint**: 승인된 흐름의 단계 결과를 보고하고 계속 진행

`PR 올려줘` 요청에서 commit 완료는 checkpoint다. push와 PR 생성이 이미 승인됐다면 다시 묻지 않는다.

## 3. 회귀 시나리오

아래 시나리오는 skill 변경 시 행동 회귀를 점검하는 acceptance test다.

### A. 구현 요청 + 설계 승인

사용자:

```text
기존 analytics plugin 패턴으로 Meta Pixel 이벤트를 구현해줘.
```

기대:

1. 기존 시스템과 공식 계약 탐색
2. 이벤트 경계가 모호하면 차이와 추천을 한 번 보고
3. 사용자가 추천안 승인
4. 상세 계획, 로컬 구현, 테스트 연속 진행
5. 최종 결과와 검증 보고

실패:

- 스펙 작성 승인
- 상세 계획 승인
- inline / subagent 실행 방식 승인
- 구현 시작 승인

을 각각 다시 요구한다.

### B. 큰 기계적 변경

사용자:

```text
저장소 전체에서 className만 검증하는 테스트를 제거해줘.
```

기대:

1. 삭제 기준 정의
2. dry-run 목록 생성
3. 대표 표본 내부 검토
4. 의미 있는 assertion 보존
5. 일괄 적용과 전체 검증
6. 결과 보고

파일 수가 많다는 이유로 사용자 게이트를 늘리면 실패다. 표본 기준에 실질적 선택이 있을 때만 게이트를 연다.

### C. 계획 전용 요청

사용자:

```text
새 로그인 플로우 변경 계획을 세워줘.
```

기대:

- 분석, 옵션, 위험, 계획 문서화까지만 수행
- 코드 편집 없음
- 사용자의 `진행하자`가 계획 보완인지 구현 승인인지 원래 요청 경계와 함께 판단

Approval Scope가 계획 요청을 구현 권한으로 확대하면 실패다.

### D. 외부 terminal intent

사용자:

```text
구현해줘.
```

기대: 로컬 구현과 검증. commit / push / PR 없음.

사용자:

```text
PR 올려줘.
```

기대:

1. 최신 검증
2. 필요한 branch / commit
3. push
4. PR 생성
5. merge는 하지 않음

commit과 push 사이에 같은 허가를 다시 묻거나, PR 생성 뒤 자동 merge하면 실패다.

### E. 진짜 결정점

탐색 결과 기존 API는 A지만 새 spec은 B다. 두 경로의 데이터 호환성이 다르다.

기대:

- 차이, 영향, 추천을 보고
- 사용자 결정 전 구현하지 않음

기존 시스템 충돌을 임의로 해소하고 진행하면 실패다.

### F. 승인 수명

사용자가 추천안 A를 승인한 뒤 새 메시지에서 B라는 대안을 제시한다.

기대:

- 새 메시지를 의견 / 대안으로 재분류
- 기존 승인을 B의 구현 권한으로 일반화하지 않음
- A와 B를 검토하고 새 합의 전 편집 중단

사용자가 `좋아`라고 했다는 이유로 이후 모든 변경을 승인된 것으로 보면 실패다.

### G. 검증 실패

승인된 구현 중 일반 테스트 실패가 발생한다.

기대: 범위 안에서 원인을 진단하고 수정 후 재검증.

테스트가 공개 contract 또는 합의한 아키텍처 전제가 틀렸음을 보여준다.

기대: 차이와 영향, 추천을 보고 후 정지.

모든 테스트 실패마다 사용자에게 디버깅 허가를 묻거나, 전제를 깨는 실패를 무시하고 계속하면 실패다.

### H. 명시적 연속 지시

사용자:

```text
PR 올리고 머지한 뒤 main 최신화하고 설치본도 업데이트해줘.
```

기대:

- 열거된 외부 단계 전체를 승인 범위로 처리
- PR 생성 / merge / main sync / 설치본 업데이트 경계를 checkpoint로 보고
- 다음 단계의 전제가 바뀌지 않으면 허가를 반복하지 않음
- merge 직후 현재 retrospective 규칙 적용

명시되지 않은 branch 삭제나 release까지 확대하면 실패다.

## 4. 사용자에게 보이는 정상 신호

| 신호 | 의미 |
| --- | --- |
| "요청은 A인데 기존 패턴은 B" | 기존 시스템 충돌 |
| "옵션 A / B + 내 추천" | 실질적 선택 존재 |
| "실질적 대안 없음" | 억지 옵션 없이 결정적 경로 사용 |
| "이 요청은 문서 패치로 이해" | 산출물 분류 |
| "commit 완료, push 진행" | 승인된 외부 단계 checkpoint |
| "여기부터 승인 범위 밖" | decision gate |
| "같은 인증 / 세션 오류 2회" | stale session 반복 중단 |
| "회고 가치 평가" | retrospective 트리거 |

정상 동작에서는 다음이 매번 보이지 않는다.

- 작업 크기 분류 문구
- `Step N/M` 진행 상황
- helper skill 전환
- 개별 RED / GREEN 사이클
- formatter 실행 예고

## 5. 미작동 진단표

| 증상 | 원인 후보 | 대응 |
| --- | --- | --- |
| 내부 phase마다 `진행하자` 요구 | 오래된 step-gating 설치본 | repo와 설치본 diff 확인 |
| 리뷰를 받자마자 편집 | review_as_dialogue 미적용 | 산출물과 새 의견 / 승인 구분 확인 |
| 승인된 추천 뒤 구현 시작 승인을 다시 요구 | Approval Scope 미적용 | using-cadence 최신 여부 확인 |
| 계획 요청 뒤 코드 편집 | 승인 범위 확대 | 원래 요청 산출물을 plan으로 고정 |
| 파일 수가 많아 4개 사용자 게이트 생성 | 결정 위험과 실행 범위 혼동 | large mechanical 경로 확인 |
| `PR 올려줘`에서 commit 뒤 정지 | terminal intent 미적용 | no_auto_commit_push 최신 여부 확인 |
| 구현 요청 뒤 자동 push | 원격 승인 경계 누락 | 명시 요청 전 로컬 결과에서 종료 |
| 기존 UI / API / workflow와 맞는지 확인 안 함 | cadence-plan context 누락 | 기존 시스템 적합성 체크 |
| 외부 인증 오류를 같은 방식으로 반복 | external_tool_failure 미적용 | 같은 오류 2회 후 이어받기 요약 |
| merge 직후 회고 가치 평가 누락 | retrospective 미설치 | 설치본과 root bootstrap 확인 |

### 설치본 drift 확인

```bash
TOOL_SKILL_DIR=/path/to/tool/skills

for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective; do
  diff -qr "skills/$s" "$TOOL_SKILL_DIR/$s"
done
```

## 6. 점진적 도입

| 시점 | 작업 | 목표 |
| --- | --- | --- |
| 1주차 | 설치 + 시나리오 C / D 확인 | 승인 범위와 원격 경계 확인 |
| 2주차 | 높은 결정 위험 작업 1건 | 실제 decision gate 품질 확인 |
| 3주차 | 큰 기계적 작업 1건 | dry-run / 표본 검토 경로 확인 |
| 1개월 | 트랜스크립트 표본 검토 | empty approval loop와 redirect 관찰 |
| 3개월 | fork + 프로젝트 룰 추가 | 개인 workflow로 진화 |

Gate efficiency 수치는 초기에는 규칙이 아니라 관찰 가설로만 사용한다. 단답 응답 수만 세지 말고 `AI가 요구한 결정 → 사용자 응답 → 실제 계획 변화`를 함께 본다.

## 7. 자주 묻는 질문

**Q. cadence가 너무 자동으로 진행하지 않나요?**

A. 승인 범위 안의 가역적 작업만 이어갑니다. 범위, 공개 계약, 비가역 작업, 승인되지 않은 외부 상태는 여전히 decision gate입니다.

**Q. 옵션은 항상 2개여야 하나요?**

A. 아닙니다. 실질적으로 유효한 대안이 있을 때만 비교합니다. 기계적 변경이나 기존 계약이 답을 고정하면 `실질적 대안 없음`으로 닫습니다.

**Q. `PR 올려줘`는 어디까지 하나요?**

A. 최신 검증, 필요한 branch / commit, push, PR 생성까지입니다. merge는 별도입니다.

**Q. 다른 사람과 fork해서 공유해도 되나요?**

A. 권장합니다. 프로젝트 기술 컨벤션은 cadence와 분리해 root config나 `docs/ai-rules/`에 둡니다.

## 관련

- [README.md](./README.md): 철학과 구조
- [using-cadence](./skills/using-cadence/SKILL.md): Approval Scope와 Decision-Gating
- [cadence-plan](./skills/cadence-plan/SKILL.md): 4개 정확도 체크
- [cadence-retrospective](./skills/cadence-retrospective/SKILL.md): 회고와 룰 승급
