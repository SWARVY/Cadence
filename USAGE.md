# cadence 운영 가이드

README 가 cadence 의 철학과 구조를 설명한다면, 이 문서는 실제 세션에서 무엇을 기대하면 되는지 보여준다.

- 처음 설치하고 작동을 확인하는 법
- 작은 / 중간 / 큰 작업에서 AI 응답이 어떻게 달라져야 하는지
- cadence 가 발동하지 않을 때 무엇을 점검할지
- 팀이나 개인 fork 에 점진적으로 도입하는 법

## 1. 처음 설치 (5분)

### 1-1. 도구 선택

사용하는 AI 도구 1+ 결정 (혼합 사용 가능). 각 도구의 공식 skill 디렉토리나 root config 위치를 확인한다.

### 1-2. 설치 옵션 — 기본 + 선택 보강

**A. `npx skills add` (Vercel skills CLI)**

```bash
npx skills add https://github.com/SWARVY/Cadence --all
```

repo 의 `skills/` 디렉토리 아래 있는 4개 skill 을 설치한다. 일부만 설치하려면 `--skill using-cadence` 처럼 선택한다.

**B. Root bootstrap 추가 (권장)**

항상 적용되어야 하는 cadence 의 최소 진입점은 프로젝트 `AGENTS.md` 또는 도구별 root config 에 짧게 둔다. 상세 절차는 skill 이 담당한다.

```markdown
항상 cadence 의 기본 리듬을 따른다: 작업 크기를 먼저 판정하고, 한 스텝 산출물만 만든 뒤 보고 후 정지한다. 사용자 피드백을 받은 다음 단계로 진행하며, 자세한 절차는 설치된 `using-cadence` / `cadence-ai-behavior` / `cadence-retrospective` skill 을 로드한다. PR merge/머지 직후에는 다음 작업 전에 `회고 가치 평가: 낮음 / 중간 / 높음` 을 먼저 출력한다.
```

**C. 수동 symlink (cross-agent 기본 위치 예시)**

```bash
git clone https://github.com/SWARVY/Cadence.git ~/Repository/Cadence

# 여러 도구가 읽을 수 있는 공통 위치를 쓰는 경우
mkdir -p ~/.agents/skills
for s in using-cadence cadence-ai-behavior cadence-plan cadence-retrospective; do
  ln -s ~/Repository/Cadence/skills/$s ~/.agents/skills/$s
done

# 특정 도구가 공식 skill 디렉토리를 따로 요구하면 그 위치에 동일하게 symlink
```

### 1-3. 작동 확인 (첫 turn 테스트)

설치 후 새 세션 열고 다음 프롬프트:

```
간단한 작업 하나 시작하고 싶어 — apps/web 에 새 컴포넌트 EmptyState 추가 검토해줘
```

AI 응답이 다음 패턴이면 cadence 작동:
- ✅ "이건 [작은/중간/큰] 작업으로 보입니다. N step 으로 진행"
- ✅ 옵션 2 안 이상 제시 + Contrarian 질문
- ✅ "기존 컴포넌트 재사용 가능?" 검토 명시

회고 게이트 회귀 테스트도 확인한다:

```
방금 PR 머지됐어. API contract 가 mid-PR 에 바뀌었고 다음 작업 시작해줘
```

AI 응답이 다음 패턴이면 회고 게이트 작동:
- ✅ "회고 가치 평가: 중간 / 높음" 을 다음 작업 안내보다 먼저 출력
- ✅ `근거` 와 `제안` 을 각각 1개 이상 포함
- ✅ `회고 처리:` 를 출력하고, 상태를 `작성`, `보류`, `생략`, `미결` 중 하나로 명시
- ✅ 중간/높음이면 처리 상태가 닫히기 전 다음 구현으로 넘어가지 않음
- ✅ 회고 파일 생성은 사용자 합의 전까지 진행하지 않음

작동 안 하면 → § 4 진단표 참조.

---

## 2. 시나리오 5가지 (실제 대화 예시)

### 시나리오 1: 작은 작업 (≤ 10분)

> **사용자**: 이 함수 변수명 `data` → `items` 로 바꿔줘

```
AI: 이건 작은 작업으로 보입니다 (rename 단일). 1 step 으로 진행하고 결과만 보고합니다.

<edit 진행>

## 결과
item-list.tsx:42 의 `data` → `items` 1건 변경. 다른 호출처 영향 없음 (grep 확인).
```

게이트 X, 보고만. 사용자 자유 응답.

---

### 시나리오 2: 중간 작업 (10–30분, 단일 feature)

> **사용자**: 설정 화면에 *활성 항목만 보기* 필터 추가하자

```
AI: 중간 작업으로 분류 — 단일 feature, 2-3 step 게이트.

## Step 1 — 컨텍스트 + 옵션
- 회고 INDEX 매칭: `settings-filter.md` 관련 회고 있음
- 기존 필터 패턴: src/settings/item-filter.tsx 에 `status` 필터 존재
- 옵션
  - A. 기존 item-filter 에 `activeOnly` 옵션 추가 (재사용)
  - B. 별도 active-filter 컴포넌트 분리 (재사용처 ≥ 2 아니면 YAGNI 위반)
- Contrarian: "활성" 기준이 서버 enum 인지 클라이언트 계산인지 — contract 확인 필요

추천: A. 의견 / redirect 받습니다.
```

→ 사용자 답변 받고 Step 2 (위험/폐기) → Step 3 (실행) 으로 진행.

---

### 시나리오 3: 큰 작업 (≥ 30분, 새 도메인 / 추상화)

> **사용자**: 리포트 내보내기 도메인 신설 — 새 src/export 폴더 + 5 페이지 라우트 + validation schemas + ...

```
AI: 큰 작업으로 분류 — 새 도메인, 4단 mandatory.

## Step 1/4 — 컨텍스트 수집
- 회고 INDEX 매칭: 검색…
- 기존 src/report 와 *export* 관계: ...
- generated client 에 export endpoint 8개 확인됨
- L2 룰 cross-check: schema/constants convention 적용 대상

검토 / 추가 컨텍스트 요청 받습니다.
```

→ 4 step 매 phase 사이 사용자 게이트. 산출물은 *스펙시트* (개요 / 동작 목록 / 엣지 케이스 / TBD / 구현 체크리스트 / 후속 작업 / 관련 회고 link).

---

### 시나리오 4: 사용자 리뷰 받기 — `review_as_dialogue` 발동

> **사용자**: item-list.tsx:78 의 `as ItemResponse` 단언 좀 그래

```
AI: 즉시 편집 대신 견해 교환부터 (review_as_dialogue 발동).

제안 검토:
- `as` 단언이 박혀있는 자리: API 응답 narrowing
- generated 타입이 union 이라 narrowing 필요한 건 맞음
- 옵션
  - A. type guard 함수 추가 (`isItemResponse`)
  - B. schema validator 로 응답 검증 → 검증된 타입 derive
  - C. discriminated union 으로 spec 재정의 요청 (server contract 의존)

내 추천: B. 신뢰 경계 (API 응답) 의 단언은 schema 가 정답.

이걸로 진행할까요?
```

→ 즉시 편집 X. 합의 후 진행.

---

### 시나리오 5: 작업 완료 후 회고

> **사용자**: 리포트 내보내기 PR 머지됐어

```
AI: 작업 완료 트리거 — cadence-retrospective 발동 검토.

회고 가치 평가: 중간
- 근거: API contract 가 mid-PR 에 한 번 바뀜
- 근거: 보조 리뷰의 type guard 권고를 schema 검증 패턴으로 거절함
- 제안: "API contract 변경은 generated client/schema 로 재검증한다" 회고 후보

회고 처리: 미결
- 추천: 작성
- 이유: 다음 작업에서 같은 contract gap 을 다시 밟을 가능성이 있음
- 다음 단계 제안: 회고를 작성/보류/생략 중 하나로 닫은 뒤 다음 작업을 시작한다.
```

→ 사용자가 작성에 동의하면 초안 → 검토 → 룰화 승급 여부 결정. 사용자가 다음 작업 우선을 명시하면 보류로 닫고 진행 가능.

> **사용자**: PR 머지하고 다음 작업 시작해줘

```
AI: PR merge 완료.

회고 가치 평가: 낮음
- 근거: 단순 문구 수정이고 새 도구/계약/협업 패턴 변화 없음
- 제안: 회고 생략

다음 작업은 ...
```

→ 다음 작업으로 이어가더라도 merge 와 다음 작업 사이의 회고 가치 평가는 생략하지 않는다.

---

## 3. cadence 발동 시그널 (사용자가 보는 것)

cadence 가 정상 작동 중이면 AI 응답에 다음 패턴 등장:

| 시그널 | 의미 |
| --- | --- |
| "이건 [작은/중간/큰] 작업으로 보입니다" | using-cadence § 1-1 작업 크기 판정 |
| "## Step N/M — <단계명>" | cadence-plan 4단 mandatory 또는 step-gating |
| "옵션 A / B / C" + "내 추천: ..." | cadence-plan § 2 옵션 2 안 + Contrarian |
| "위험: ... / 폐기 조건: ... / Out of scope: ..." | cadence-plan § 3 mandatory |
| "즉시 편집 대신 견해 교환부터" | review_as_dialogue 발동 |
| "이걸로 진행할까요?" / 자유 응답 권유 | step-gating 게이트 |
| "회고 가치 평가: 낮음 / 중간 / 높음" | cadence-retrospective 트리거. PR merge 직후에는 파일 생성 여부와 별개로 mandatory |
| "근거 없는 단정" / "확인 안 하고 가정했어요" | collaborator_not_authority 자기 비판 |

---

## 4. cadence 미작동 진단표

| 증상 | 원인 후보 | 대응 |
| --- | --- | --- |
| AI 가 사용자 의견 받자마자 *즉시 편집* 시작 | review_as_dialogue skill 미매칭 또는 미설치 | symlink 확인. 도구가 별도 메모리를 쓰면 `install.sh` 또는 root config 로 보강 |
| AI 가 *옵션 1 안* 만 제출 | cadence-plan § 2 미발동 | "작업 크기 판정해줘 + 옵션 2 안 이상" 명시 요청 |
| AI 가 *자동 commit/push* 진행 | no_auto_commit_push 미매칭 | symlink + 강한 자동화는 hook 등록 |
| AI 가 작업 시작 시 *크기 판정* 안 함 | using-cadence § 0 첫 점검 누락 | description 매칭 실패 — hook 등록 검토 |
| AI 가 *반사적 동의* (사용자 의견에 무조건 동의) | collaborator_not_authority 미매칭 | "내 의견 검토해줘, 반대면 주장해줘" 명시 |
| PR merge 직후 회고 가치 평가를 출력하지 않음 | cadence-retrospective 미설치 또는 using-cadence 의 merge→next chain 함정 | symlink 확인. "머지 후 회고 가치 평가부터" 명시 |
| repo 의 skill 수정이 실제 세션에 반영되지 않음 | repo `skills/` 와 도구별 설치본 drift | 아래 `diff -q` 로 설치본 최신 여부 확인. 다르면 재설치 또는 symlink 갱신 |

### 작동 점검 빠른 체크

```bash
# cross-agent 기본 위치
ls -l ~/.agents/skills/ | grep cadence

# 도구별 공식 위치를 쓰는 경우 해당 skill 디렉토리 확인
TOOL_SKILL_DIR=/path/to/tool/skills
ls -l "$TOOL_SKILL_DIR" | grep cadence

# repo 의 source 와 설치본이 같은지 확인
diff -q skills/using-cadence/SKILL.md "$TOOL_SKILL_DIR"/using-cadence/SKILL.md
diff -q skills/cadence-retrospective/SKILL.md "$TOOL_SKILL_DIR"/cadence-retrospective/SKILL.md

# 별도 프로젝트 메모리 경로를 쓰는 경우
CADENCE_MEMORY_DIR=/path/to/tool/memory ~/Repository/Cadence/skills/cadence-ai-behavior/install.sh --dry-run
```

---

## 5. 점진적 도입 (1주 / 2주 / 1개월)

| 주차 | 작업 | 목표 |
| --- | --- | --- |
| **1주차** | symlink 설치 + 한 작업 의식적 트리거 | 작동 확인 / AI 응답 패턴 관찰 |
| **2주차** | 큰 작업 1건 + 4단 mandatory 의식적 follow | cadence-plan 의 step-gating cadence 익숙해지기 |
| **3주차** | 회고 1건 작성 + 룰화 승급 검토 | cadence-retrospective 사이클 학습 |
| **1개월 후** | 트랜스크립트 마이닝 (주기적) | recurring 패턴 → 룰 추가 사이클 |
| **3개월 후** | 자기 fork + 커스텀 룰 추가 | cadence 의 *진짜 가치* — 개인 워크플로우로 진화 |

---

## 6. 자주 묻는 질문

**Q. cadence 가 너무 무거워요. 작은 작업까지 게이트 통과?**
A. 의도된 동작 아닙니다. § 1-1 *작업 크기 판정* 이 작동하면 작은 작업은 1 step. 안 작동하면 § 4 진단표 참조.

**Q. AskUserQuestion 으로 매번 물어보는데 부담돼요.**
A. using-cadence § 7-2 의 *AskUserQuestion 강요 함정*. cadence 가 제대로 작동하면 *자유 응답* 받아야 정상. "옵션 4지선다 그만, 그냥 의견 들려줘" 한 번 명시.

**Q. cadence 룰 중 일부만 쓰고 싶어요.**
A. 각 skill 은 *독립* 발동. symlink 안 걸면 그 skill 만 skip.

**Q. 다른 사람과 fork 해서 공유해도 되나요?**
A. 권장. `skills/cadence-*` / `skills/using-cadence` 는 cross-agent 표준이라 fork 시 *자기 선호로 수정* 후 자체 repo 로 publish. README § 룰 작성 가이드 따르면 일관성 유지.

---

## 관련

- [README.md](./README.md) — 구조 / 설치 / 룰 작성 가이드
- [using-cadence/SKILL.md](./skills/using-cadence/SKILL.md) — 메타 라우팅 / 우선순위 / step-gating 상세
- [cadence-plan/SKILL.md](./skills/cadence-plan/SKILL.md) — 4단 mandatory + 스펙시트 메타-구조
- [cadence-retrospective/SKILL.md](./skills/cadence-retrospective/SKILL.md) — 회고 + 룰화 승급
- [Skills.sh directory](https://www.skills.sh/) — Vercel 의 agent skills 디렉토리
