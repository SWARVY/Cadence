---
name: 주 도구 ↔ 보조 도구 크로스 체크
description: 기능 구현 완료 시점에 주 AI 도구의 판단을 다른 모델 family 또는 독립 리뷰 경로로 검증한다. 단일 모델 편향을 줄이고, 도구 조합은 프로젝트 환경에 맞춘다.
type: feedback
---

기능 구현이 완료되고 검증(브라우저/테스트 등)까지 끝나면, 사용자에게 결과를 보고하기 전에 **독립된 보조 리뷰 경로** 로 크로스 체크할 필요가 있는지 검토한다. 보조 리뷰 경로가 프로젝트에 설정되어 있어도 결정 위험과 검증 비용에 비례해 실행하며, 사용자가 명시적으로 "크로스 체크" 를 요청하면 수행한다. 검토 단위는 plan task가 아니라 [cadence-plan의 review slice](../../cadence-plan/SKILL.md#review-topology-preflight)다.

**Why:** 단일 모델 편향 회피. 버그/엣지케이스, 코드 스타일/베스트 프랙티스, 아키텍처 적합성은 모델이나 리뷰 경로마다 잘 보는 지점이 다르다.

**보조 리뷰 경로 예시:**

| 주 도구 | 보조 경로 후보 | 실행 방식 |
| --- | --- | --- |
| 대화형 코딩 에이전트 | 다른 모델 family 의 CLI / IDE agent | 도구별 review 명령 또는 독립 세션 |
| IDE agent | 터미널 기반 agent / PR review bot | 외부 CLI 호출 또는 PR 코멘트 확인 |
| PR review bot 중심 흐름 | 로컬 agent self-review | PR 코멘트 triage 전후 보완 |
| 기타 | 적어도 *다른 모델 family* 하나 | 프로젝트가 가진 리뷰 도구 사용 |

**How to apply:**

- **Trigger (조건부 후보)**: 판단 위험이 있는 review slice 구현 + L1 검증 완료 → 사용자에게 완료 보고 직전 보조 리뷰 경로 실행 필요성을 검토
- **Trigger (수동)**: "크로스 체크", "다른 도구로 리뷰" 등 사용자 요청 시 즉시 실행
- **실행 방식**: 현재 주 도구와 독립적인 모델 family 또는 리뷰 경로를 선택한다. 특정 CLI 명령은 프로젝트/도구 환경에 맞춘다.
- **결과 처리**: 보조 도구 출력 *전체 노출 X*. 의미 있는 지적만 요약 + 각 지적에 대한 *내 의견* (동의/반대/보류) 함께 제시. 반영 여부는 사용자가 결정
- **false positive 주의**: 보조 도구가 지적해도 무조건 수정 X. 기존 프로젝트 룰과 충돌하면 *내 의견으로 반박*
- **단위 edit·plan task마다 실행 X** — 같은 불변식과 증거를 공유하는 task는 하나의 review slice로 묶는다.
- **비용 비례**: 낮은 위험의 작은 변경이 결정론적 검증을 통과하면 추가 AI 리뷰를 생략할 수 있다. 기본 상한은 독립 semantic 검토 1개다.
- **상위 경로 진입**: 1차 검토 불일치, 높은 결정 위험, 큰 blast radius, 여러 기능 누적, 사용자 명시 요청일 때만 추가 모델 family나 PR bot 경로를 연다.
- **PR 직전/PR 중 재검토**: 여러 기능이 누적됐거나 새 PR bot 코멘트가 달려 current code 기준 판단이 달라질 수 있을 때만 다시 triage
- **재리뷰 범위**: load-bearing finding을 수정해 결론이 달라질 때만 수정 diff를 scoped re-review한다. style·format·경로 같은 기계적 항목은 해당 검사 결과로 닫는다.
- **하위 workflow 충돌**: plan header나 workflow가 task별 reviewer를 요구해도 사용자가 그 topology를 명시하지 않았다면 현재 위험 기반 slice가 우선한다.

**3-path는 상위 단계:** 로컬 self-review + 다른 모델 family + PR review bot 조합은 높은 위험이나 검토 불일치를 해소할 때 유효하다. 같은 결론을 반복 확인하기 위한 기본 절차로 사용하지 않는다.

근거: [리뷰 단위와 위험 경계 회고](../../../notes/2026-08-09-review-unit-risk-boundary-gap.md)
