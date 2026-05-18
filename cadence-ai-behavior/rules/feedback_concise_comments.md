---
name: 주석은 간결하게
description: 장황한 주석 블록 회피 — 핵심만 한두 줄, 코드가 자명한 부분은 주석 생략
type: feedback
---
코드 주석은 **핵심만 한두 줄**로 작성한다. 다단 설명, 단계별 나열, 자명한 코드를 그대로 한국어로 옮겨 적는 주석은 피한다.

**Why:** 주석이 길면 가독성이 떨어지고 코드와 함께 stale 되기 쉽다. 비-자명한 의도/이유만 캡처하면 충분.

**How to apply:**
1. JSDoc 헤더로 함수 인자/리턴/예외를 나열하지 않는다 — 타입 시그니처가 답한다.
2. "단계 1, 단계 2" 식 절차 나열 주석 → 의도 한 줄로 줄이거나 코드만 남긴다.
3. 컨벤션·라이브러리 동작 (예: "valibot 의 partialCheck 는 ...") 은 *비-자명한* 동작만 한 줄로 메모.
4. 제목/섹션 구분용 주석 (`// === SECTION ===`) 은 실제 구분 가치가 클 때만.

**Examples (피드백 라운드 직전 → 후):**

```ts
// 직전 — 8줄 JSDoc
/**
 * 진입 가드:
 * 1. verify 게이트에서 발급받은 authenticatedKey 보유 — 부재 시 verify 게이트로 재유도
 * 2. 자체 로그인 회원만 — providerType 이 있으면 (OAuth) root 로 차단
 *
 * 가드는 component 가 마운트되기 전 beforeLoad 에서 처리해, 본 페이지는 항상 정상
 * 상태(키 보유 + 자체 로그인) 만 가정한다.
 */

// 후 — 1줄
// beforeLoad 가드: authenticatedKey 보유 + 자체 로그인만 허용. 위반은 redirect.
```

```ts
// 직전 — 4줄 inline 코멘트
// 첫 blur 까지는 silent, 이후 onChange — 입력 중 새 비밀번호 확인 필드의
// "일치하지 않음" 에러가 매 글자마다 깜빡이는 UX 손실을 줄인다.

// 후 — 1줄
// 첫 blur 후 onChange — confirm 필드 입력 중 깜빡임 방지
```
