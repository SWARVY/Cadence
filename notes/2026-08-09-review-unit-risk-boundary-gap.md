---
title: 리뷰 단위는 계획 task가 아니라 독립적으로 실패할 수 있는 위험 경계여야 한다
date: 2026-08-09
status: draft
related-skills:
  - using-cadence
  - cadence-plan
  - cadence-ai-behavior
related-rules:
  - feedback_crosscheck
related-retrospectives:
  - ./2026-08-04-transition-preflight-enforcement-gap.md
---

# 리뷰 단위는 계획 task가 아니라 독립적으로 실패할 수 있는 위험 경계여야 한다

## 무엇이 일어났나

여러 단계로 나눈 리팩터링 계획을 task별 subagent 실행과 독립 리뷰 흐름에 연결했다. 계획의 각 task는 작업 순서와 진행 상태를 표현하기에는 유용했지만, 모두가 독립적인 판단이나 결함 위험을 가진 것은 아니었다.

초기 문서 task에는 semantic 리뷰와 재리뷰가 반복됐다. 실행 가능한 경로 검사처럼 실제 결함을 잡은 지적도 있었지만, 이후 검토는 예제 코드의 인용부호처럼 결정론적 검사로 닫을 수 있는 항목까지 같은 리뷰 루프에 남겼다. 검토 비용이 구현 가치보다 커진 뒤에야 후속 task를 여러 묶음으로 합치고, 기계적 검증과 마지막 whole-change 리뷰 중심으로 전환했다.

전환 뒤에도 구조 경계, 동작 보존, 정적 검사와 전체 회귀를 확인할 수 있었다. 이는 task별 semantic 리뷰가 품질의 필수 조건이 아니라, 실제 위험 경계와 검증 수단을 잘못 매핑한 결과였음을 보여 줬다.

## 왜 일어났나 (근본 원인)

### 1. 계획 task와 review unit을 같은 단위로 취급했다

계획 task는 순서, 인계, 진행 추적을 위한 단위다. 반면 review unit은 한 reviewer가 같은 불변식과 증거로 승인하거나 거부할 수 있는 단위다. 서로 목적이 다른데도 `task 완료 → 독립 reviewer`를 고정 연결했다.

그 결과 같은 아키텍처 불변식을 공유하는 연속 이동 작업은 여러 번 다시 설명됐고, 문서·설정·format처럼 결정론적으로 판정 가능한 변경에도 semantic 판단 비용이 붙었다.

### 2. 하위 workflow의 절차를 실행 시점의 비용 판단보다 강하게 적용했다

Cadence에는 낮은 위험의 변경을 L1 검증과 표본 확인으로 닫고, 불일치나 높은 위험에서만 상위 검토로 올라가는 비용 사다리가 있었다. 하지만 하위 workflow가 task별 review를 요구할 때 어느 규칙이 review topology를 소유하는지 명확하지 않았다.

### 3. 재리뷰 종료 조건이 위험 해소가 아니라 finding 소진이었다

첫 리뷰에서 발견된 항목을 모두 닫는 것이 루프의 목표가 되면서, formatter나 정적 검사로 확인 가능한 잔여 항목도 reviewer를 다시 호출했다. load-bearing finding과 기계적 품질 항목을 구분하지 않았다.

### 4. 계획의 상세도가 독립 검토 표면을 불필요하게 키웠다

계획이 실제 구현 계약보다 파일 목록, 예제 코드, 단계별 명령을 반복할수록 reviewer가 검사할 문서 표면도 커졌다. 세부 표현의 불일치가 제품 위험과 같은 gate에 들어가면서 비용이 증폭됐다.

## 어떻게 해결했나

Cadence가 실행 전에 task 수가 아니라 **review slice**를 정하도록 규칙을 보강했다.

- **Execution task**: 작업 순서, 인계, 진행 추적 단위
- **Review slice**: 동일한 위험·불변식·검증 증거로 함께 승인하거나 거부할 수 있는 변경 묶음
- **Commit unit**: history에서 독립적으로 설명하거나 되돌릴 가치가 있는 단위

세 단위는 같을 수 있지만 자동으로 같다고 가정하지 않는다.

review slice별 기본 검증은 다음처럼 둔다.

| 변경 성격 | 기본 검증 | semantic review |
| --- | --- | --- |
| 문구·경로·format·기계적 이동 | 정적 검사, diff 표본, 관련 test | 기본 생략 |
| 동일 불변식을 공유하는 구조·통합 변경 | 관련 test, typecheck/build, 경계 검색 | slice 완료 후 targeted 1회 |
| 공개 계약·보안·데이터·migration | 계약 증거와 실패 경로 검증 | 위험 경계마다 targeted 1회 |
| 여러 slice가 누적된 큰 변경 | 전체 회귀와 실제 runtime 확인 | 필요 시 whole-change 1회 |

재리뷰는 수정으로 판단이 달라질 수 있는 load-bearing finding에 한정한다. style, formatting, 경로 존재 여부처럼 결정론적으로 판정 가능한 항목은 해당 검사 결과로 닫는다. Minor finding은 현재 위험을 키우지 않으면 ledger나 최종 검토로 넘긴다.

## 다음에 어떻게 예방할까

1. 계획 header의 특정 workflow 지시는 실행 전략 후보로 취급하고, 사용자의 명시적 task별 리뷰 요청으로 확대하지 않는다.
2. 실행 preflight에서 task 간 결합도, 공유 불변식, 변경 위험, 검증 증거를 기준으로 review slice를 만든다.
3. reviewer가 인접 task 하나는 승인하고 다른 task는 독립적으로 거부할 수 있을 때만 task 경계를 review 경계로 사용한다.
4. 기계적 task는 별도 semantic reviewer 없이 L1과 표본 diff로 닫는다.
5. 재리뷰 전에 남은 finding이 실제 결론을 바꾸는지 확인한다.
6. subagent 수, review 횟수, plan phase 수를 품질 지표로 사용하지 않는다.

## 수용 기준

- 여러 plan task가 같은 아키텍처 불변식과 검증을 공유하면 하나의 review slice로 묶는다.
- 낮은 위험의 문서·format·경로 변경은 결정론적 검증이 통과하면 별도 AI reviewer를 호출하지 않는다.
- 하위 workflow가 task별 review를 요구해도 Cadence가 현재 위험과 비용에 맞게 실행 topology를 조정한다.
- 사용자에게 task별 review를 명시적으로 요청받은 경우에는 그 범위를 따른다.
- 재리뷰는 load-bearing finding의 수정 범위만 확인하고, 기계적 항목은 검사 결과로 닫는다.
- 큰 변경의 최종 whole-change review는 앞선 task별 리뷰 횟수와 무관하게 실제 누적 위험이 있을 때만 수행한다.

## 룰화 승급 검토

- [x] `using-cadence`: 하위 workflow보다 현재 review topology preflight가 우선함을 명시
- [x] `cadence-plan`: plan task와 review slice 분리, 위험 기반 검증 매핑
- [x] `cadence-ai-behavior`: 독립 검토와 재리뷰 비용 상한 보강
- [ ] 프로젝트별 ai-rules: 프로젝트 종속 규칙으로 둘 필요 없음

새 skill을 만들지 않는다. 사용자 게이트와 workflow 소유권은 `using-cadence`, 위험·검증 설계는 `cadence-plan`, 보조 리뷰 실행 규칙은 `feedback_crosscheck`가 각각 소유한다.
