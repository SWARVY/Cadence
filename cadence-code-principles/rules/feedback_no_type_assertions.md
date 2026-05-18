---
name: 타입 단언(as) 금지
description: auto-generated 코드 외에는 `as` 단언을 쓰지 않는다. 스키마 검증 또는 타입 가드로 안전하게 좁힌다.
type: feedback
---

TypeScript `as` 단언은 **타입 검사를 우회** 하는 마지막 수단이다. 사용처에서 단언이 보이면 *자료구조 결함 신호* 로 간주하고 구조 변경으로 해소한다.

**Why:** 단언은 "지금 이 자리에서는 맞다" 는 인간 주장일 뿐, 리팩터 / 스키마 변경 시 컴파일러 보호를 잃는다. 단언이 *반복적으로* 필요하다면 데이터 모양 자체가 잘못된 신호.

**How to apply:**

1. **스키마로 좁히기** — 외부 입력 (폼 / API 응답 / URL search params 등 신뢰 경계) 은 valibot / zod 같은 스키마로 통과시킨 뒤 `InferOutput` 타입 사용. `as` 단언하지 말 것.
2. **타입 가드 함수** — `function isApiError(e: unknown): e is ApiError { ... }` 같은 user-defined type guard 로 narrowing. discriminated union 의 `kind` / `type` 필드 분기는 TypeScript control flow 가 자동으로 좁혀줌 — `as` 불필요.
3. **자료구조 재설계** — 단언이 반복적이라면 `Partial<Record<K, V>>` 대신 `Record<K, V | undefined>`, discriminated union 도입, 옵셔널 chaining 등으로 해소.
4. **예외 (허용):**
   - 자동 생성 코드 — 건드리지 않음
   - 라이브러리 타입 정의가 잘못된 경우 — `as` 대신 가능하면 `@ts-expect-error` + 사유 주석 (좁은 경계)
   - 테스트 fixture 의 partial mock — `as Partial<T>` 정도까지, production 코드에는 금지
5. **`@ts-expect-error` 의 좁은 경계** — *타입 거짓말이 불가피한 한 줄* 에만 사용. 페이지 / 함수 전체에 두지 않음.
6. **크로스 체크 도구가 단언 발견 시** — false positive 가 아닌 한 즉시 구조 변경
