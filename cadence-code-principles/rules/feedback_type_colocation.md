---
name: 타입 co-location 선호
description: types.ts 별도 파일 대신 컴포넌트 / 모듈 파일에 타입을 co-locate
type: feedback
---

타입은 사용하는 *모듈* 과 가까이 둔다. 다른 레이어에서 재사용되지 않는다면 별도 `types.ts` 를 만들지 않는다.

**Why:** 타입과 사용처 사이 거리가 멀어지면 *코드 탐색 비용* 증가. 단일 모듈 전용 타입이 공용 파일에 섞이면 *관리 단위* 가 흐려진다.

**How to apply:**

- 단일 컴포넌트 / 모듈에서만 쓰는 타입 → 해당 파일에 정의
- 여러 모듈에서 공유 → *공통 파일* 에 export (예: `<domain>-common.ts`)
- `types.ts` 는 *정말 많은 곳에서 import* 할 때만 생성 (대략 3+ 파일)
