# Reference-selection v1 호출 계약

선택적 연결 패키지가 참조 선택을 제공할 때 사용한다. 전송 방식은 패키지가 정하고, 요청과 결과의 의미는 이 문서가 소유한다.

요청:

```json
{
  "contract_version": 1,
  "task": "reference-selection",
  "language": "ko",
  "summary": "설정의 저장과 재시작 후 복원을 검증한다.",
  "references": [
    {"id": "verification", "description": "실제 저장과 재조회 검증", "required": true}
  ]
}
```

ID는 고유한 불투명 식별자이며 실행할 경로나 명령이 아니다. `required`는 메인 에이전트가 현행 규칙에 따라 정한다. 도구는 이를 변경하지 않는다. 패키지는 지원 언어·입력 크기를 명시하고 초과 입력을 조용히 자르는 대신 fallback한다.

성공 결과는 `contract_version: 1`, `task: reference-selection`, `status: advisory`, `mode`, `items`, `selected_ids`, `fallback`을 포함한다. `items`는 요청 ID마다 하나씩 `id`, `decision: include | exclude | abstain`, 근거를 담는다. 근거는 설명문 또는 `reason_code`로 표현하며 생성하지 않은 설명을 만들어 넣지 않는다. confidence·확률·도구 식별자·실행 시간은 선택 필드다. `selected_ids`는 include 항목과 정확히 일치하고 필수 ID를 모두 포함해야 한다.

실패 결과는 `contract_version: 1`, `status: fallback`, `reason_code`, `fallback: baseline`을 반환한다. 실패한 실행의 부분 추천은 사용하지 않는다. 미지원 task·버전·언어, 누락된 설정, 잘못된 출력도 기본 경로로 복귀한다.

메인 에이전트는 ID 집합·필수 항목 보존·출력 형식을 확인한다. 시험 운용의 `mode: shadow`는 추천과 무관하게 기본 선택을 수행하며 `fallback: baseline`을 유지한다. 추천의 정확도나 성능 개선은 실제 평가에서 별도로 확인한다.
