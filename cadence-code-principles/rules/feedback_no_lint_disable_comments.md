---
name: 린트 규칙 무시 주석 지양
description: eslint-disable / oxlint-disable 주석으로 린트 경고를 덮지 말고 코드 구조를 바꿔 원인을 제거한다
type: feedback
---

린트 경고는 disable 주석으로 덮지 말고 *구조 변경* 으로 해소한다. 예: `key` 에 index 만 쓰면 경고 → `eslint-disable-next-line react/no-array-index-key` 대신 `` key={`${item.label}-${index}`} `` 처럼 discriminator 조합.

예외는 자동 생성 파일과 라이브러리 버그 / 외부 제약으로 회피 불가능한 경우로 한정하며, 후자는 반드시 *사유 주석* 과 함께 기재.

**Why:** 대부분의 린트 경고는 코드를 조금만 바꾸면 해소되므로 주석으로 덮는 것은 *기술 부채*. disable 주석은 *원인 미해소* 신호.

**How to apply:**

- 린트 경고 발생 시 먼저 *구조 변경* 으로 해소 가능한지 검토
- `key` 에 index 가 잡히면 고유값 (ID > 유니크 텍스트 > `${value}-${index}` 조합) 으로 바꿈
- 자동 생성 코드 / 외부 제약이 아닌 곳에서는 disable 주석 추가 금지
- 예외 적용 시 반드시 *사유 주석* 한 줄
